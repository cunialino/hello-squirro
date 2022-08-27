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
        if host and port:
            self.client = Elasticsearch("http://{host}:{port}".format(host, port))
        else:
            self.client = Elasticsearch()
    def insert_file(self, index: str, id: str, document: typing.Mapping[str, typing.Any]) -> typing.Optional[ObjectApiResponse[typing.Any]]:
        try:
            resp = self.client.index(index=index, id=id, document=document)
            return resp
        except Exception as e:
            self.logger.critical("Failed to insert document: {}".format(e))


