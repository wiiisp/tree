from arbre import Trie
from arbre_substitution import TrieSubstitution
from arbre_add_remove import TrieAddRemove
from  threading import Thread
import pika
import time
import json

def threaded(func):
    """
    Decorator that multithreads the target function
    with the given parameters. Returns the thread
    created for the function
    """
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.start()
        return thread
    return wrapper

def handle(channel, arbre, data):
    if data["arbre"].get("search"):
        print("heloo", type(arbre))
        mot = data["arbre"].get("search")
        exist = arbre.search(mot)
        channel.basic_publish(exchange='',
                    routing_key='arbre_manipulation',
                    body=exist)
    

@threaded
def loop_rabbit():
    # Example
    # arbre = Trie()
    arbre = TrieSubstitution(errors=2)
    arbre.insert("diplodocus")
    
    # Connection rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='arbre_manipulation')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("it's working", data)
        # handle(channel, arbre, data)

    channel.basic_consume(queue='arbre_manipulation', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


    

def main():

    
    loop_rabbit()


    # trie = TrieSubstitution(errors=2)
    # trie.insert("hello")
    # trie.insert("helio")
    # trie.insert("helfo")
    # trie.insert("world")
    # print(trie.search("hemtp"))  # Output: True
    # print(trie.search("world"))  # Output: True
    # print(trie.search("python")) # Output: False
    # trie.delete("world")
    # print(trie.search("world"))  # Output: False

    # trie = Trie()
    # trie.insert("hello")
    # trie.insert("world")
    # print(trie.search("hello"))  # Output: True
    # print(trie.search("world"))  # Output: True
    # print(trie.search("python")) # Output: False
    # trie.delete("world")
    # print(trie.search("world"))  # Output: False

    # Ajout/suppression de caractere OU substitution
    trie = TrieAddRemove(errors=3)
    trie.insert("hello")
    # trie.insert("world")
    print(trie.search("hello"))  # Output: True
    # print(trie.search("world"))  # Output: True
    # print(trie.search("python")) # Output: False
    # trie.delete("world")
    # print(trie.search("world"))  # Output: False


if __name__ == "__main__":
    main()
