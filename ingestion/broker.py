import os
import pika


def connection():
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "marketlane"),
        os.getenv("RABBITMQ_PASSWORD", "marketlane"),
    )
    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=credentials,
    )
    return pika.BlockingConnection(parameters)


def declare_queue(channel):
    queue = os.getenv("RABBITMQ_QUEUE", "marketlane.events")
    channel.queue_declare(queue=queue, durable=True)
    return queue
