import logging
import os

from datetime import datetime
from elasticsearch import Elasticsearch

from defaults import ELASTIC_DEFAULT_INDEX, ELASTICSEARCH_DSL, ELASTIC_USER, ELASTIC_PASSWD

class ElasticClient():

    def __init__(self):
        self.client = Elasticsearch(
            hosts=ELASTICSEARCH_DSL['default']['hosts'],
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWD),
            timeout=ELASTICSEARCH_DSL['default']['timeout']
        )

    def create_machine_info(self, disk_info: dict, mem_info: dict, battery_info: dict):
        doc = {
            "timestamp": datetime.now(),
            "machine": os.getenv('NAME'),
            "disk_info": disk_info,
            "memory_info": mem_info,
            "battery_info": battery_info
        }
        resp = self.client.index(index=ELASTIC_DEFAULT_INDEX, document=doc)
        logging.info(f'Info registered into ElasticSearch')
