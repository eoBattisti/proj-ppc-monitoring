import os

ELASTIC_DEFAULT_INDEX = 'monitoring'

ELASTIC_USER = os.getenv('ELASTICSEARCH_USERNAME', None)
ELASTIC_PASSWD = os.getenv('ELASTICSEARCH_PASSWORD', None)
ELASTIC_PORT = os.getenv('ELASTICSEARCH_PORT', None)
ELASTIC_HOST = os.getenv('ELASTICSEARCH_HOST', None)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://{user}:{password}@{host}:{port}/'.format(user=ELASTIC_USER,
                                                                  password=ELASTIC_PASSWD,
                                                                  host=ELASTIC_HOST,
                                                                  port=ELASTIC_PORT),
        'timeout': 30,
    },
}
