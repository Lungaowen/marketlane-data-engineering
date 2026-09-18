import json
import os
import time

import psycopg

from events.contracts import BookingCreated
from ingestion.broker import connection, declare_queue
from transformations.booking import to_fact_booking


def warehouse_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "marketlane_warehouse"),
        user=os.getenv("POSTGRES_USER", "marketlane"),
        password=os.getenv("POSTGRES_PASSWORD", "marketlane"),
    )


def wait_for_warehouse():
    for _ in range(30):
        try:
            return warehouse_connection()
        except psycopg.OperationalError:
            time.sleep(2)
    raise RuntimeError("Warehouse did not become available")


def process_event(ch, method, properties, body):
    payload = json.loads(body)
    event_type = payload.get("event")

    if event_type != "booking.created":
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    event = BookingCreated.model_validate(payload)
    fact = to_fact_booking(event)

    with warehouse_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO raw_events (event_type, payload)
                VALUES (%s, %s)
                """,
                (event_type, json.dumps(payload)),
            )
            cur.execute(
                """
                INSERT INTO warehouse.fact_bookings
                    (booking_id, vendor_id, customer_id, amount, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (booking_id) DO NOTHING
                """,
                (
                    fact["booking_id"],
                    fact["vendor_id"],
                    fact["customer_id"],
                    fact["amount"],
                    fact["created_at"],
                ),
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
