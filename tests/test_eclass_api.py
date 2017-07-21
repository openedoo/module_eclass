import json
import unittest
from openedoo_project import app


class EclassApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_empty_eclass_collection(self):
        eclass = self.client.get('/api/v1/eclass')
        data = json.loads(eclass.data)
        self.assertEqual(eclass.status_code, 200)
        self.assertEqual(data, "[]")
