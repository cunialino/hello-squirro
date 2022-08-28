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

    def create_index(self, index: str, mappings: typing.Mapping[str, typing.Any], settings: typing.Mapping[str, int]) -> None:
        if not self.client.indices.exists(index=index):
            self.client.indices.create(index=index, mappings=mappings, settings=settings)

    def delete_index(self, index: str) -> None:
        if self.client.indices.exists(index=index):
            self.client.indices.delete(index=index)

    def insert_file(self, index: str, document: typing.Mapping[str, str], id: typing.Optional[str] = None) -> typing.Optional[str]:
        try:
            resp = self.client.index(index=index, document=document, id=id)
            self.logger.info("inserted {}".format(resp['_id']))
            return resp[ '_id' ]
        except Exception as e:
            self.logger.critical("Failed to insert document: {}".format(e))

    def get_file(self, index: str, id: str) -> typing.Optional[ObjectApiResponse[typing.Any]]:
        try:
            doc = self.client.get_source(index=index, id=id)
            self.logger.info("retrieved {}".format(doc))
            return doc
        except Exception as e:
            self.logger.critical("Failed to retrieve document: {}".format(e))
