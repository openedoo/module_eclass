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

    def test_get_an_eclass_by_id_returns_empty_when_not_found(self):
        eclass = self.client.get('api/v1/eclass/99999999')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('[]', str(eclass.data))

    def test_succesfully_update_an_eclass(self):
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

        new_cs_name = {
            'name': 'computer engineering'
        }
        update_cs = self.client.put('api/v1/eclass/1',
                                    data=json.dumps(new_cs_name),
                                    content_type='application/json')
        self.assertEqual(update_cs.status_code, 200)
        self.assertIn('success', str(update_cs.data))

        eclass = self.client.get('api/v1/eclass/1')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('computer engineering', str(eclass.data))

    def test_succesfuly_delete_an_eclass(self):
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

        delete_eclass = self.client.delete('api/v1/eclass/1')
        self.assertEqual(delete_eclass.status_code, 200)
        self.assertIn('success', str(delete_eclass.data))

        eclass = self.client.get('api/v1/eclass/1')
        self.assertEqual(eclass.status_code, 200)
        self.assertIn('[]', str(eclass.data))

    def test_successfuly_add_member_to_an_eclass(self):
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
        student = {
            'user_id': 67
        }
        member = self.client.post('api/v1/eclass/1/members',
                                  data=json.dumps(student),
                                  content_type='application/json')
        self.assertEqual(member.status_code, 200)
        self.assertIn('success', str(member.data))

        member = self.client.get('api/v1/eclass/1/members')
        self.assertEqual(member.status_code, 200)
        self.assertIn('67', str(member.data))

    def test_add_member_to_an_eclass_failed_with_415_status_code(self):
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

        member = self.client.post('api/v1/eclass/1/members',
                                  content_type='application/json')
        self.assertEqual(member.status_code, 415)
        self.assertIn('Failed to load request data', str(member.data))

    def test_successfuly_delete_a_member_from_eclass(self):
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
        student = {
            'user_id': 67
        }
        member = self.client.post('api/v1/eclass/1/members',
                                  data=json.dumps(student),
                                  content_type='application/json')
        self.assertEqual(member.status_code, 200)
        self.assertIn('success', str(member.data))

        member = self.client.get('api/v1/eclass/1/members')
        self.assertEqual(member.status_code, 200)
        self.assertIn('67', str(member.data))

        leave_eclass = self.client.delete('api/v1/eclass/1/members/67')
        self.assertEqual(leave_eclass.status_code, 200)
        self.assertIn('success', str(leave_eclass.data))

    def test_successfuly_add_discussion_in_an_eclass(self):
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

        discussion = {
            'user_id': 999999,
            'description': "Something about a discusion here ~!@#$%^*()_+"
        }
        add_discussion = self.client.post('api/v1/eclass/1/discussions',
                                          data=json.dumps(discussion),
                                          content_type='application/json')
        self.assertEqual(add_discussion.status_code, 200)
        self.assertIn('success', str(add_discussion.data))

    def test_get_discussion_in_eclass(self):
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

        discussion = {
            'user_id': 999999,
            'description': "Something about a discusion here ~!@#$%^*()_+"
        }
        add_discussion = self.client.post('api/v1/eclass/1/discussions',
                                          data=json.dumps(discussion),
                                          content_type='application/json')
        self.assertEqual(add_discussion.status_code, 200)
        self.assertIn('success', str(add_discussion.data))

        discussions = self.client.get('api/v1/eclass/1/discussions')
        self.assertEqual(discussions.status_code, 200)
        self.assertIn('Something about a discusion here', str(discussions.data))
