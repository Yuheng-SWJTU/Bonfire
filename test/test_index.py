import unittest
from app import app
import json


class TestBuildCamp(unittest.TestCase):

    """
    Total: 9
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # login user
        data = {'email': 'zzh@bilgin.top', 'password': '20020207yh'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def tearDown(self):
        # logout user
        response = self.app.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_empty_name(self):
        data = {'camp_name': '', 'description': 'test it out'}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_empty_description(self):
        data = {'camp_name': 'test', 'description': ''}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_empty_name_and_description(self):
        data = {'camp_name': '', 'description': ''}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_duplication(self):
        data = {'camp_name': 'ttttt', 'description': 'test it out'}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_exceed_camp_name(self):
        max_length = 21
        data = {'camp_name': 'a' * max_length, 'description': 'test it out'}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_exceed_camp_name_empty_description(self):
        max_length = 21
        data = {'camp_name': 'a' * max_length, 'description': ''}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_exceed_camp_name_exceed_description(self):
        max_length_name = 21
        max_length_des = 201
        data = {'camp_name': 'a' * max_length_name, 'description': 'a' * max_length_des}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_exceed_description(self):
        max_length = 201
        data = {'camp_name': 'test', 'description': 'a' * max_length}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_build_camp_exceed_description_empty_name(self):
        max_length = 201
        data = {'camp_name': '', 'description': 'a' * max_length}
        response = self.app.post('/buildcamp', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class TestJoinCamp(unittest.TestCase):

    """
    Total: 2
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # login user
        data = {'email': 'zzh@bilgin.top', 'password': '20020207yh'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def tearDown(self):
        # logout user
        response = self.app.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_join_camp_empty_camp_id(self):
        data = {'camp_id': ''}
        response = self.app.post('/join_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_join_camp_repeatedly(self):
        data = {'camp_id': '2'}
        response = self.app.post('/join_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'You are already in the camp.')


if __name__ == '__main__':
    unittest.main()
