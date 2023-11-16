import sys
import threading
import pika
from infoExtract import *
from tinydb import TinyDB
import os

db_lock = threading.Lock()


def consume_urls_from_queue(threadsNrParam):
    def callback(ch, method, properties, body):
        url = body.decode('utf-8')
        data = extractInfoFromPage(url)

        if data is not None:
            with db_lock:
                db.insert(data)
            print(f"Processed URL: {url} by {threading.current_thread().name}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consumer_thread():
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='url_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='url_queue', on_message_callback=callback)

        print(f"Consumer is waiting for messages. To exit press CTRL+C (Thread: {threading.current_thread().name})")
        channel.start_consuming()

    threadsNr = threadsNrParam
    threads = []

    for i in range(threadsNr):
        thread = threading.Thread(target=start_consumer_thread, name=f"Thread({i})")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    fileName = sys.argv[1]
    threadsNrInput = sys.argv[2]
    db = TinyDB(f'{fileName}.json')
    consume_urls_from_queue(int(threadsNrInput))
