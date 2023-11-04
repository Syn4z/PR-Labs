import pika
import requests
import time
from consumer import *
from parseLinks import *


def send_urls_to_queue(urls):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='url_queue')

    for url in urls:
        channel.basic_publish(exchange='', routing_key='url_queue', body=url)
        print(f"Sent URL: {url}")

    connection.close()


if __name__ == "__main__":
    start_url = "https://interauto.md/automobile"
    urls = parseLinks(start_url, 5)
    send_urls_to_queue(urls)
