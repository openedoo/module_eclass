import json
import unittest
from openedoo_project import app, db


class EclassApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_empty_eclass_collection(self):
        eclass = self.client.get('/api/v1/eclass')
        data = json.loads(eclass.data)
        self.assertEqual(eclass.status_code, 200)
        self.assertEqual(data, "[]")

    def test_create_eclass_failed_with_415_status_code(self):
        com_science_eclass = {
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT'
        }
        create_eclass = self.client.post('api/v1/eclass',
                                         data=json.dumps(com_science_eclass))
        self.assertEqual(create_eclass.status_code, 415)
        self.assertIn('Failed to load request data', str(create_eclass.data))

    def test_create_eclass_failed_with_400_status_code(self):
        com_science_eclass = {
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT'
        }
        create_eclass = self.client.post('api/v1/eclass',
                                         data=json.dumps(com_science_eclass),
                                         content_type='application/json')
        self.assertEqual(create_eclass.status_code, 400)
        self.assertIn('Missing request parameter', str(create_eclass.data))
