import json
import time

import pika
from sqlalchemy.orm import sessionmaker

from services.shared.db import engine
from services.shared.models import Unit
from services.shared.messaging import publish_message
from services.allocation_service.app.allocator import required_unit_type, choose_best_unit


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            connection.close()
            print("Connected to RabbitMQ")
            return
        except Exception:
            print("RabbitMQ not ready, retrying in 2 seconds...")
            time.sleep(2)


def process_event(ch, method, properties, body):
    try:
        payload = json.loads(body)
        print(f"Received event.created: {payload}")

        event_id = payload["event_id"]
        event_type = payload["event_type"]
        event_x = payload["location_x"]
        event_y = payload["location_y"]
        severity = payload["severity"]

        needed_type = required_unit_type(event_type)
        if not needed_type:
            print(f"No unit mapping found for event type: {event_type}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        db = SessionLocal()
        try:
            candidate_units = (
                db.query(Unit)
                .filter(Unit.unit_type == needed_type, Unit.status == "available")
                .all()
            )

            best_unit = choose_best_unit(candidate_units, event_x, event_y)

            if not best_unit:
                print(f"No available unit found for event {event_id}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            dispatch_payload = {
                "event_id": event_id,
                "unit_id": best_unit.id,
                "unit_type": best_unit.unit_type.value if hasattr(best_unit.unit_type, "value") else str(best_unit.unit_type),
                "priority": severity,
                "attempt": 1,
            }

            publish_message("dispatch.requested", dispatch_payload)
            print(f"Published dispatch.requested: {dispatch_payload}")

        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing event: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    wait_for_rabbitmq()

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            channel = connection.channel()

            channel.exchange_declare(exchange="ddcs", exchange_type="topic", durable=True)
            channel.queue_declare(queue="allocation.event.created", durable=True)
            channel.queue_bind(
                exchange="ddcs",
                queue="allocation.event.created",
                routing_key="event.created",
            )

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue="allocation.event.created",
                on_message_callback=process_event,
            )

            print("Allocation service waiting for event.created messages...")
            channel.start_consuming()

        except Exception as e:
            print(f"Allocation service connection error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()