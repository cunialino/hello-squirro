from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
import logging
import os
import typing

class ESDatabase:
    __LOGGING_FORMAT = "[%(asctime)s] Elasticsearch database: %(message)s"
    logging.basicConfig(format=__LOGGING_FORMAT)
    def __init__(self) -> None:
        self.logger = logging.getLogger("logs")
        self.logger.setLevel(20)
        host = os.environ.get('ES_HOST_STRING')
        port = os.environ.get('ES_PORT')
        if host is None and port is None:
            host = "localhost"
            port="9200"
        self.client = Elasticsearch("http://{host}:{port}".format(host=host, port=port), request_timeout=300)
        if not self.client.indices.exists(index="hellosquirro"):
            self.create_index()

    def create_index(self):
        mappings = {
            "properties": {
                "file_name": {"type": "text"},
                "text": {"type": "text"},
                "summary": {"type": "text"}
            }
        }
        setting = {
            "number_of_shards": 1, 
            "number_of_replicas": 1
        }
        self.client.indices.create(index="hellosquirro", mappings=mappings, settings=setting)

    def insert_file(self, index: str, id: str, document: typing.Mapping[str, typing.Any]) -> typing.Optional[ObjectApiResponse[typing.Any]]:
        try:
            resp = self.client.index(index=index, id=id, document=document)
            return resp
        except Exception as e:
            self.logger.critical("Failed to insert document: {}".format(e))


