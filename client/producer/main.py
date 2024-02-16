import argparse
import dotenv
import datetime
import os
from typing import Dict, List

import orjson
import pika


settings = dotenv.load_dotenv('./env-sample.env')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'rabbitmq')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'admin')

def transform_str(data: str, machine: str) -> List[Dict]:
    _data = []
    for line in data.split('\n'):
        _raw_data = line.split(' ')
        _value = _raw_data[1]
        _metric, _extra_info = _raw_data[0].split('{')
        _extra_info = _extra_info.split(',')
        _data.append({
            "machine": machine,
            "metric": _metric,
            "process": _extra_info[0].split('=')[1].replace('"', ''),
            "pid": _extra_info[1].split('=')[1].replace('"', '').replace('}', ''),
            "value": float(_value),
            "datetime": datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        })
    return _data

def main(data: List[Dict]) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_URL,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='sp-monitoring') # 'sp-monitoring' stands for 'server process monitoring'
    channel.basic_publish(exchange='',
                          routing_key='sp-monitoring',
                          body=orjson.dumps(data))
    connection.close()


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--data', type=str)
    args.add_argument('--machine', type=str)

    args = args.parse_args()

    data = transform_str(data=args.data, machine=args.machine)
    main(data=data)
