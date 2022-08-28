import unittest
from squirro.db import ESDatabase
from datetime import datetime

class TestIO(unittest.TestCase):

    def setUp(self) -> None:
        self.db = ESDatabase()
        self.doc = {
            'text': 'Elasticsearch db unittests'
        }
        self.index = "hellosquirro"
        self.es_id = "testid"
        self.db.delete_index(self.index)
        self.db.create_index(index=self.index, mappings={'properties': {'text': {'type': 'text'}}}, settings={'number_of_shards': 1, 'number_of_replicas': 1})

    def test_insert_document(self):
        idx = self.db.insert_file(self.index, self.doc)
        self.assertNotEqual(idx, None)

    def test_get_document(self):
        idx = self.db.insert_file(self.index, self.doc)
        if idx is not None:
            res = self.db.get_file(self.index, id=idx)
            self.assertNotEqual(res, None)

if __name__ == "__main__":
    unittest.main()
