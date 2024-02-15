import datetime
import logging
import sys
import os
from typing import Dict, List

import pika
import orjson
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'admin')

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://elasticsearch:9200')
ELASTICSEARCH_USER = os.environ.get('ELASTICSEARCH_USER', 'elastic')
ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD', 'elastic')

ELASTICSEARCH_INDEX = 'sp-monitoring'


def send_data_to_elk(ch, method, properties, body: bytes):
    es = Elasticsearch(ELASTICSEARCH_URL, basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD))
    _body: List[Dict] = orjson.loads(body)
    _data = [{
        "_index": ELASTICSEARCH_INDEX,
        "_source": orjson.dumps(process),
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    } for process in _body if process.get('value') != 0]
    sucess, errors  = bulk(es, _data, raise_on_error=True)
    if not sucess:
        logging.info("An error occured: %s", errors)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        ))
    channel = connection.channel()
    channel.queue_declare(queue='sp-monitoring')
    channel.basic_consume(queue='sp-monitoring', on_message_callback=send_data_to_elk, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
