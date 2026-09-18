import json
import os
import time
from datetime import datetime, timezone

import pika

from ingestion.broker import connection, declare_queue


payload = {
    "event": "booking.created",
    "bookingId": "booking-demo-001",
    "vendorId": "vendor-demo-001",
    "customerId": "customer-demo-001",
    "amount": 350.0,
    "createdAt": datetime.now(timezone.utc).isoformat(),
}

for attempt in range(20):
    try:
        conn = connection()
        break
    except pika.exceptions.AMQPConnectionError:
        if attempt == 19:
            raise
        time.sleep(2)

channel = conn.channel()
queue = declare_queue(channel)
channel.basic_publish(
    exchange="",
    routing_key=queue,
    body=json.dumps(payload).encode(),
    properties=pika.BasicProperties(delivery_mode=2),
)
print(f"Published {payload['event']} to {queue}")
conn.close()
