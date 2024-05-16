from arbre import Trie
from arbre_substitution import TrieSubstitution
from arbre_add_remove import TrieAddRemove
from threading import Thread
import pika
import json


def handle(channel, props, arbre, data):
    if data["arbre"].get("search"):
        mot = data["arbre"]["search"]
        exist = arbre.search(mot)
        channel.basic_publish(
            exchange="",
            routing_key="arbre_manipulation",
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=str(exist),
        )
        return channel
    elif data["arbre"].get("insert"):
        mot = data["arbre"]["insert"]
        arbre.insert(mot)
        msg = f"Mot {mot} inséré dans l'arbre"
        channel.basic_publish(
            exchange="",
            routing_key="arbre_manipulation",
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=msg,
        )
        print(f" [x] Done with the msg: {msg}")
        return channel
    else:
        mot = data["arbre"].get("delete")
        res = arbre.delete(mot)
        msg = f"Mot {mot} supprimé de l'arbre"
        channel.basic_publish(
            exchange="",
            routing_key="arbre_manipulation",
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=msg,
        )
        print(f" [x] Done with the msg: {msg}")
        return channel


def loop_rabbit():
    # Example
    # arbre = Trie()
    arbre = TrieSubstitution(errors=2)
    arbre.insert("diplodocus")

    # Connection rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="arbre_manipulation")

    def callback(ch, method, props, body):
        data = json.loads(body)
        print(f"Receiving the data {data}, now we process it...")
        ch = handle(channel, props, arbre, data)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="arbre_manipulation", on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def main():
    loop_rabbit()


if __name__ == "__main__":
    main()
