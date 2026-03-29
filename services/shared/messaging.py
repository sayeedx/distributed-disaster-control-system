import json
import os
from typing import Any

import pika


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EVENTS_QUEUE = "event.created"


class RabbitPublisher:
    def __init__(self) -> None:
        self.params = pika.URLParameters(RABBITMQ_URL)

    def publish(self, queue_name: str, payload: dict[str, Any]) -> None:
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        connection.close()
