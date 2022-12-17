import unittest
from app import app
import json


class TestAddCategory(unittest.TestCase):
    """
    Total: 18
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

    def test_add_category_repeated(self):
        data = {'camp_id': '4', 'category_name': 'test', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'This category has been added!')

    def test_add_category_empty_camp_id(self):
        data = {'camp_id': '', 'category_name': 'test', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_add_category_empty_category_name(self):
        data = {'camp_id': '4', 'category_name': '', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please check your input!')

    def test_add_category_empty_category_color(self):
        data = {'camp_id': '4', 'category_name': 'test', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'This category has been added!')

    def test_add_category_empty_camp_id_and_category_name(self):
        data = {'camp_id': '', 'category_name': '', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_add_category_empty_camp_id_and_category_color(self):
        data = {'camp_id': '', 'category_name': 'test', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_add_category_empty_category_name_and_category_color(self):
        data = {'camp_id': '4', 'category_name': '', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please check your input!')

    def test_add_category_empty_camp_id_and_category_name_and_category_color(self):
        data = {'camp_id': '', 'category_name': '', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_add_category_exceed_max_length(self):
        max_length = 21
        data = {'camp_id': '4', 'category_name': 'a' * max_length, 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please check your input!')

    def test_add_category_exceed_max_length_and_empty_category_color(self):
        max_length = 21
        data = {'camp_id': '4', 'category_name': 'a' * max_length, 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please check your input!')

    def test_add_category_exceed_max_length_and_empty_camp_id(self):
        max_length = 21
        data = {'camp_id': '', 'category_name': 'a' * max_length, 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_add_category_exceed_max_length_and_empty_camp_id_and_category_color(self):
        max_length = 21
        data = {'camp_id': '', 'category_name': 'a' * max_length, 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission(self):
        data = {'camp_id': '1', 'category_name': 'test', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_category_name(self):
        data = {'camp_id': '1', 'category_name': '', 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_category_color(self):
        data = {'camp_id': '1', 'category_name': 'test', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_category_name_and_category_color(self):
        data = {'camp_id': '1', 'category_name': '', 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_exceed_max_length(self):
        max_length = 21
        data = {'camp_id': '1', 'category_name': 'a' * max_length, 'category_color': 'blue'}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_exceed_max_length_and_empty_category_color(self):
        max_length = 21
        data = {'camp_id': '1', 'category_name': 'a' * max_length, 'category_color': ''}
        response = self.app.post('/camp/add_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")


class TestEditCategory(unittest.TestCase):
    """
    Total: 45
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

    def test_edit_empty_category_name(self):
        data = {'category_id': '5', 'category_name': '', 'category_color': 'blue', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_color(self):
        data = {'category_id': '5', 'category_name': 'test', 'category_color': '', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_name_and_category_color(self):
        data = {'category_id': '5', 'category_name': '', 'category_color': '', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_camp_id(self):
        data = {'category_id': '5', 'category_name': 'test', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id_and_camp_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_name_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_name_and_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id_and_category_name_and_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id_and_category_name_and_category_color(self):
        data = {'category_id': '', 'category_name': '', 'category_color': '', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id_and_category_name_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_empty_category_id_and_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name(self):
        max_length = 21
        data = {'category_id': '5', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_id(self):
        max_length = 21
        data = {'category_id': '', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_camp_id(self):
        max_length = 21
        data = {'category_id': '5', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_id_and_camp_id(self):
        max_length = 21
        data = {'category_id': '', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_id_and_category_color(self):
        max_length = 21
        data = {'category_id': '', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_id_and_category_color_and_camp_id(self):
        max_length = 21
        data = {'category_id': '', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_color(self):
        max_length = 21
        data = {'category_id': '5', 'category_name': 'a' * max_length, 'category_color': '', 'camp_id': '4'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_edit_exceed_category_name_empty_category_color_and_camp_id(self):
        max_length = 21
        data = {'category_id': '5', 'category_name': 'a' * max_length, 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission(self):
        data = {'category_id': '6', 'category_name': 'test', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_camp_id(self):
        data = {'category_id': '6', 'category_name': 'test', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_id_and_camp_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_id_and_category_color(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_id_and_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': 'test', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_color(self):
        data = {'category_id': '6', 'category_name': 'test', 'category_color': '', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_color_and_camp_id(self):
        data = {'category_id': '6', 'category_name': 'test', 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name(self):
        data = {'category_id': '6', 'category_name': '', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_camp_id(self):
        data = {'category_id': '6', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_color(self):
        data = {'category_id': '6', 'category_name': '', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_color_and_camp_id(self):
        data = {'category_id': '6', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_id_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_id_and_category_color(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_empty_category_name_and_category_id_and_category_color_and_camp_id(self):
        data = {'category_id': '', 'category_name': '', 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_categ0ry_name(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_camp_id(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_color(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': '', 'camp_id': '1'}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_color_and_camp_id(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': '', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_id(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_id_and_camp_id(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_id_and_category_color(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_permission_exceed_category_name_and_category_id_and_category_color_and_camp_id(self):
        max_length = 21
        data = {'category_id': '6', 'category_name': 'a' * max_length, 'category_color': 'blue', 'camp_id': ''}
        response = self.app.post('/camp/editcategory', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class TestDeleteCategory(unittest.TestCase):
    """
    Total test cases: 5
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

    def test_permission_empty_category_id(self):
        data = {'category_id': ''}
        response = self.app.post('/camp/delete_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_category_id_and_camp_id(self):
        data = {'category_id': '', 'camp_id': ''}
        response = self.app.post('/camp/delete_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_category_id(self):
        data = {'category_id': '100'}
        response = self.app.post('/camp/delete_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_category_id_and_camp_id(self):
        data = {'category_id': '100', 'camp_id': '100'}
        response = self.app.post('/camp/delete_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_camp_id(self):
        data = {'category_id': '6', 'camp_id': '100'}
        response = self.app.post('/camp/delete_category', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")


class TestLeaveCamp(unittest.TestCase):
    """
    Total test cases: 4
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

    def test_permission_empty_camp_id(self):
        data = {'camp_id': ''}
        response = self.app.post('/camp/leave_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_camp_id(self):
        data = {'camp_id': '100'}
        response = self.app.post('/camp/leave_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_camp_you_are_not_in(self):
        data = {'camp_id': '1'}
        response = self.app.post('/camp/leave_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")


class TestAddAdmin(unittest.TestCase):
    """
    Total test cases: 8
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

    def test_permission_empty_camp_id(self):
        data = {'camp_id': '', 'username': 'Bilgin'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_camp_id_and_empty_username(self):
        data = {'camp_id': '', 'username': ''}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_username(self):
        data = {'camp_id': '1', 'username': ''}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_camp_id(self):
        data = {'camp_id': '100', 'username': 'Bilgin'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_username(self):
        data = {'camp_id': '6', 'username': 'qwer'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The user is not exist!")

    def test_user_does_not_in_camp(self):
        data = {'camp_id': '6', 'username': 'Bilgin'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "This user is not in this camp!")

    def test_user_is_already_admin(self):
        data = {'camp_id': '4', 'username': 'Bilgin'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "This user is already an admin!")

    def test_add_admin_empty_camp_id(self):
        data = {'camp_id': '', 'username': 'Bilgin'}
        response = self.app.post('/camp/add_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")


class TestRemoveAdmin(unittest.TestCase):
    """
    Total: 6
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

    def test_permission_empty_camp_id(self):
        data = {'camp_id': '', 'admin_id': '3'}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_camp_id_and_empty_admin_id(self):
        data = {'camp_id': '', 'admin_id': ''}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_permission_empty_admin_id(self):
        data = {'camp_id': '1', 'admin_id': ''}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_camp_id(self):
        data = {'camp_id': '100', 'admin_id': '3'}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_nonexistent_admin_id(self):
        data = {'camp_id': '6', 'admin_id': '100'}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The user is not exist!")

    def test_user_is_not_admin(self):
        data = {'camp_id': '6', 'admin_id': '1'}
        response = self.app.post('/camp/remove_admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "This user is not in this camp!")


class TestUploadBackground(unittest.TestCase):

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

    def test_upload_none(self):
        data = {'camp_id': '6', 'file': None}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Please deliver your background image first! ")

    def test_upload_empty_camp_id(self):
        data = {'camp_id': '', 'file': None}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Please deliver your background image first! ")

    def test_upload_nonexistent_camp_id(self):
        data = {'camp_id': '100', 'file': None}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Please deliver your background image first! ")

    def test_upload_empty_camp_id_and_file(self):
        file = open('resources/test_large.jpg', 'rb')
        data = {'camp_id': '', 'file': (file, 'test_large.jpg')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The size of the file is too big! ")

    def test_upload_nonexistent_camp_id_and_file(self):
        file = open('resources/test_large.jpg', 'rb')
        data = {'camp_id': '100', 'file': (file, 'test_large.jpg')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The size of the file is too big! ")

    def test_upload_empty_camp_id_and_file2(self):
        file = open('resources/test_pdf.pdf', 'rb')
        data = {'camp_id': '', 'file': (file, 'test_pdf.pdf')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The format of the file is wrong! ")

    def test_upload_nonexistent_camp_id_and_file2(self):
        file = open('resources/test_pdf.pdf', 'rb')
        data = {'camp_id': '100', 'file': (file, 'test_pdf.pdf')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The format of the file is wrong! ")

    def test_upload_pdf(self):
        file = open('resources/test_pdf.pdf', 'rb')
        data = {'camp_id': '6', 'file': (file, 'test_pdf.pdf')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The format of the file is wrong! ")

    def test_upload_large(self):
        file = open('resources/test_large.jpg', 'rb')
        data = {'camp_id': '6', 'file': (file, 'test_large.jpg')}
        response = self.app.post('/camp/upload_background', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The size of the file is too big! ")


class TestEditCamp(unittest.TestCase):

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

    def test_edit_empty_camp_id(self):
        data = {'camp_id': '', 'camp_name': 'test', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_name(self):
        data = {'camp_id': '6', 'camp_name': '', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp name can't be empty!")

    def test_edit_empty_camp_description(self):
        data = {'camp_id': '6', 'camp_name': 'test', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp description can't be empty!")

    def test_edit_empty_camp_id_and_empty_camp_name(self):
        data = {'camp_id': '', 'camp_name': '', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_id_and_empty_camp_description(self):
        data = {'camp_id': '', 'camp_name': 'test', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_name_and_empty_camp_description(self):
        data = {'camp_id': '6', 'camp_name': '', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp name can't be empty!")

    def test_edit_empty_camp_id_and_empty_camp_name_and_empty_camp_description(self):
        data = {'camp_id': '', 'camp_name': '', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_no_permission(self):
        data = {'camp_id': '1', 'camp_name': 'test', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_no_permission_empty_camp_name(self):
        data = {'camp_id': '1', 'camp_name': '', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_no_permission_empty_camp_description(self):
        data = {'camp_id': '1', 'camp_name': 'test', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_no_permission_empty_camp_name_and_empty_camp_description(self):
        data = {'camp_id': '1', 'camp_name': '', 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_camp_name_exist(self):
        data = {'camp_id': '6', 'camp_name': 'ttttt', 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp name is already exist!")

    def test_edit_exceed_camp_name(self):
        max_length = 21
        data = {'camp_id': '6', 'camp_name': 'a' * max_length, 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the camp name is too long!")

    def test_edit_exceed_camp_description(self):
        max_length = 101
        data = {'camp_id': '6', 'camp_name': 'test', 'camp_description': 'a' * max_length}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the camp description is too long!")

    def test_edit_empty_camp_id_exceed_camp_name(self):
        max_length = 21
        data = {'camp_id': '', 'camp_name': 'a' * max_length, 'camp_description': 'test'}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_id_exceed_camp_description(self):
        max_length = 101
        data = {'camp_id': '', 'camp_name': 'test', 'camp_description': 'a' * max_length}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_id_exceed_camp_name_and_exceed_camp_description(self):
        max_length = 101
        data = {'camp_id': '', 'camp_name': 'a' * max_length, 'camp_description': 'a' * max_length}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "You don't have the permission!")

    def test_edit_empty_camp_name_exceed_camp_description(self):
        max_length = 101
        data = {'camp_id': '6', 'camp_name': '', 'camp_description': 'a' * max_length}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp name can't be empty!")

    def test_edit_empty_camp_description_exceed_camp_name(self):
        max_length = 21
        data = {'camp_id': '6', 'camp_name': 'a' * max_length, 'camp_description': ''}
        response = self.app.post('/camp/edit_camp', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The camp description can't be empty!")


class TestMakePost(unittest.TestCase):
    """
    Total: 15
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

    def test_empty_title(self):
        data = {'title': '', 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_content(self):
        data = {'title': 'test', 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_empty_category_id(self):
        data = {'title': 'test', 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The category is not exist!")

    def test_empty_title_and_content(self):
        data = {'title': '', 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_title_and_category_id(self):
        data = {'title': '', 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_content_and_category_id(self):
        data = {'title': 'test', 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_empty_title_and_content_and_category_id(self):
        data = {'title': '', 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_title_exceed_max_length(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too long!")

    def test_title_exceed_max_length_and_empty_content(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_exceed_max_length_and_empty_category_id(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too long!")

    def test_title_exceed_max_length_and_empty_content_and_category_id(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_less_min_length(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too short!")

    def test_title_less_min_length_and_empty_content(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_less_min_length_and_empty_category_id(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too short!")

    def test_title_less_min_length_and_empty_content_and_category_id(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/make_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")


class TestFavorite(unittest.TestCase):
    """
    Total: 3
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

    def test_post_non_exist(self):
        data = {'post_id': '999999'}
        response = self.app.post('/camp/favorite', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post does not exist.")

    def test_post_exist(self):
        data = {'post_id': '1'}
        response = self.app.post('/camp/favorite', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Cancel favorite")

    def test_post_exist_clicked(self):
        data = {'post_id': '1'}
        response = self.app.post('/camp/favorite', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Favorite success.")


class TestLike(unittest.TestCase):
    """
    Total: 3
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

    def test_post_non_exist(self):
        data = {'post_id': '999999'}
        response = self.app.post('/camp/like', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post does not exist.")

    def test_post_exist(self):
        data = {'post_id': '1'}
        response = self.app.post('/camp/like', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Cancel like")

    def test_post_exist_clicked(self):
        data = {'post_id': '1'}
        response = self.app.post('/camp/like', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Like success.")


class TestDelete(unittest.TestCase):
    """
    Total: 1
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

    def test_delete_non_exist(self):
        data = {'post_id': '999999'}
        response = self.app.post('/camp/delete_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post does not exist.")


class TestComment(unittest.TestCase):
    """
    Total: 3
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

    def test_post_non_exist(self):
        data = {'post_id': '999999', 'content': 'test'}
        response = self.app.post('/camp/comment', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post does not exist.")

    def test_post_no_content(self):
        data = {'post_id': '1', 'content': ''}
        response = self.app.post('/camp/comment', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Comment content cannot be empty.")

    def test_post_non_exist_empty_content(self):
        data = {'post_id': '99999', 'content': ''}
        response = self.app.post('/camp/comment', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Comment content cannot be empty.")


class TestDeleteComment(unittest.TestCase):
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

    def test_delete_non_exist(self):
        data = {'comment_id': '999999'}
        response = self.app.post('/camp/delete_comment', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The comment does not exist.")


class TestUploadImage(unittest.TestCase):

    """
    Total: 3
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

    def test_none_file(self):
        data = {'wangeditor-uploaded-image': None}
        response = self.app.post('/camp/upload_image', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Image cannot be empty.")

    def test_pdf_file(self):
        file = open('resources/test_pdf.pdf', 'rb')
        data = {'wangeditor-uploaded-image': (file, 'test_pdf.pdf')}
        response = self.app.post('/camp/upload_image', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Image format error.")

    def test_large_file(self):
        file = open('resources/test_large.JPG', 'rb')
        data = {'wangeditor-uploaded-image': (file, 'test_large.jpg')}
        response = self.app.post('/camp/upload_image', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "Image size cannot be more than 2M.")


class TestEditPosts(unittest.TestCase):

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

    def test_empty_title(self):
        data = {'title': '', 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_content(self):
        data = {'title': 'test', 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_empty_category_id(self):
        data = {'title': 'test', 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The category is not exist!")

    def test_empty_title_and_content(self):
        data = {'title': '', 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_title_and_category_id(self):
        data = {'title': '', 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_empty_content_and_category_id(self):
        data = {'title': 'test', 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_empty_title_and_content_and_category_id(self):
        data = {'title': '', 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post title can't be empty!")

    def test_title_exceed_max_length(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too long!")

    def test_title_exceed_max_length_and_empty_content(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_exceed_max_length_and_empty_category_id(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too long!")

    def test_title_exceed_max_length_and_empty_content_and_category_id(self):
        max_length = 51
        data = {'title': 'a' * max_length, 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_less_min_length(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': 'test and test', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too short!")

    def test_title_less_min_length_and_empty_content(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': '', 'category_id': '6', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")

    def test_title_less_min_length_and_empty_category_id(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': 'test and test', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The length of the post title is too short!")

    def test_title_less_min_length_and_empty_content_and_category_id(self):
        min_length = 1
        data = {'title': 'a' * min_length, 'content': '', 'category_id': '', 'description': 'test',
                'is_notice': 'false', 'is_top': 'false'}
        response = self.app.post('/camp/edit_post', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], "The post content can't be empty!")


# class
if __name__ == '__main__':
    unittest.main()
