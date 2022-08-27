import unittest
from squirro.db import ESDatabase
from datetime import datetime

class TestIO(unittest.TestCase):

    def setUp(self) -> None:
        self.db = ESDatabase()
        self.doc = {
            'file_name': 'unitTest',
            'text': 'Elasticsearch db unittests',
            'sumamry': '',
        }
        self.index = "hellosquirro"
        self.es_id = '1'

    def test_insert_document(self):
        res = self.db.insert_file(self.index, self.es_id, self.doc)
        self.assertNotEqual(res, None)

if __name__ == "__main__":
    unittest.main()
