import pika
import time
import json

BODY = {
    "arbre": {"search": "diplodocus"}
}

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    result = channel.queue_declare(queue='arbre_manipulation')
    callback_queue = result.method.queue
    channel.basic_publish(exchange='',
                        routing_key='arbre_manipulation',
                        properties=pika.BasicProperties(
                                reply_to = callback_queue,
                                ),
                        body=json.dumps(BODY))
    time.sleep(0.5)
    
    def callback(ch, method, properties, body):
        print(f"[x] Le mot existe il : {['oui' if body else 'non']}")

    channel.basic_consume(queue='arbre_manipulation', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for  server response. To exit press CTRL+C')
    channel.start_consuming()



if __name__ == "__main__":
    main()
