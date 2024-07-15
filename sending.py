import pika
import time
import json
import uuid

BODY = {"arbre": {"search": "dimplodocus"}}


class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="arbre_manipulation")
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.corr_id:
            self.response = body.decode()

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="arbre_manipulation",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body),
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


def main():
    client = RabbitClient()
    print(f" [x] Envoi de requête au consommateur: {BODY}")
    response = client.call(BODY)
    print(f" [.] Reponse du consommateur: {response}")


if __name__ == "__main__":
    main()
