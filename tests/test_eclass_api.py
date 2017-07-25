import sys
import json
import unittest
from openedoo_project import app, db


class EclassApiTest(unittest.TestCase):
    def setUp(self):
        if not app.config['TESTING']:
            sys.exit()

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

    def test_successfuly_create_eclass(self):
        com_science_eclass = {
            'user_id': 56,
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_eclass = self.client.post('api/v1/eclass',
                                         data=json.dumps(com_science_eclass),
                                         content_type='application/json')
        self.assertEqual(create_eclass.status_code, 200)

    def test_get_eclass_collection(self):
        com_science_eclass = {
            'user_id': 56,
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_cs_eclass = self.client.post('api/v1/eclass',
                                            data=json.dumps(com_science_eclass),
                                            content_type='application/json')
        self.assertEqual(create_cs_eclass.status_code, 200)

        biology_eclass = {
            'user_id': 999,
            'name': 'Biology',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_biology_eclass = self.client.post('api/v1/eclass',
                                    data=json.dumps(biology_eclass),
                                    content_type='application/json')
        self.assertEqual(create_biology_eclass.status_code, 200)

        eclass = self.client.get('api/v1/eclass')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('computer science', str(eclass.data))
        self.assertIn('Biology', str(eclass.data))

    def test_get_eclass_collection_by_creator(self):
        com_science_eclass = {
            'user_id': 56,
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_cs_eclass = self.client.post('api/v1/eclass',
                                            data=json.dumps(com_science_eclass),
                                            content_type='application/json')
        self.assertEqual(create_cs_eclass.status_code, 200)

        biology_eclass = {
            'user_id': 999,
            'name': 'Biology',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_biology_eclass = self.client.post('api/v1/eclass',
                                    data=json.dumps(biology_eclass),
                                    content_type='application/json')
        self.assertEqual(create_biology_eclass.status_code, 200)

        eclass = self.client.get('api/v1/eclass?creator_id=999')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('Biology', str(eclass.data))

    def test_get_eclass_collection_by_member(self):
        com_science_eclass = {
            'user_id': 999,
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_cs_eclass = self.client.post('api/v1/eclass',
                                            data=json.dumps(com_science_eclass),
                                            content_type='application/json')
        self.assertEqual(create_cs_eclass.status_code, 200)

        biology_eclass = {
            'user_id': 999,
            'name': 'Biology',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_biology_eclass = self.client.post('api/v1/eclass',
                                    data=json.dumps(biology_eclass),
                                    content_type='application/json')
        self.assertEqual(create_biology_eclass.status_code, 200)

        eclass = self.client.get('api/v1/eclass?member_id=999')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('computer science', str(eclass.data))
        self.assertIn('Biology', str(eclass.data))

    def test_get_an_eclass_by_id(self):
        com_science_eclass = {
            'user_id': 999,
            'name': 'computer science',
            'university': 'Yogyakarta International University',
            'course': 'IT',
            'privilege': 'public'
        }
        create_cs_eclass = self.client.post('api/v1/eclass',
                                            data=json.dumps(com_science_eclass),
                                            content_type='application/json')
        self.assertEqual(create_cs_eclass.status_code, 200)
        eclass = self.client.get('api/v1/eclass/1')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('computer science', str(eclass.data))
