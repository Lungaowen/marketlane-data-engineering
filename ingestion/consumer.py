import json
import os
import time

import clickhouse_connect
from events.contracts import BookingCreated
from ingestion.broker import connection, declare_queue
from transformations.booking import to_fact_booking


def warehouse_client():
    return clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST", "localhost"),
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USER", "marketlane"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "marketlane"),
        database=os.getenv("CLICKHOUSE_DATABASE", "warehouse"),
    )


def wait_for_warehouse():
    for _ in range(30):
        try:
            client = warehouse_client()
            client.command("SELECT 1")
            return client
        except Exception:
            time.sleep(2)
    raise RuntimeError("ClickHouse did not become available")


def process_event(ch, method, properties, body):
    payload = json.loads(body)
    event_type = payload.get("event")

    if event_type != "booking.created":
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    event = BookingCreated.model_validate(payload)
    fact = to_fact_booking(event)

    ch_client = warehouse_client()
    ch_client.insert(
        "warehouse.raw_events",
        [[event_type, json.dumps(payload)]],
        column_names=["event_type", "payload"],
    )
    ch_client.insert(
        "warehouse.fact_bookings",
        [[
            fact["booking_id"],
            fact["vendor_id"],
            fact["customer_id"],
            fact["amount"],
            fact["created_at"],
        ]],
        column_names=["booking_id", "vendor_id", "customer_id", "amount", "created_at"],
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    wait_for_warehouse().close()
    conn = connection()
    channel = conn.channel()
    queue = declare_queue(channel)
    channel.basic_qos(prefetch_count=10)
    channel.basic_consume(queue=queue, on_message_callback=process_event)

    print(f"Consuming Marketlane events from {queue}")
    channel.start_consuming()


if __name__ == "__main__":
    main()
