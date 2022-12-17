import unittest
from app import app
import json


class TestLogin(unittest.TestCase):

    """
    Total test cases: 14
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_empty_username_password(self):
        data = {'emails': '', 'password': ''}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username(self):
        data = {'email': '', 'password ': '123456'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_password(self):
        data = {'email': 'test@123.com', 'password ': ''}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_username_password(self):
        data = {'email': 'test@123.com', 'password': '123456'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_wrong_characters_username_password(self):
        data = {'email': 'test@', 'password': '[];:|'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_username(self):
        data = {'email': 'test@', 'password': '123456'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_password(self):
        data = {'email': 'i@bilgin.top', 'password': '[];:|'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_exceed_max_length_username(self):
        max_length = 51
        max_email = 'a' * max_length + '@gmail.com'
        data = {'email': max_email, 'password': '123456'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_exceed_max_length_password(self):
        max_length = 41
        max_password = 'a' * max_length
        data = {'email': 'i@bilgin.top', 'password': max_password}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_exceed_max_length_username_password(self):
        max_length = 51
        max_email = 'a' * max_length + '@gmail.com'
        max_length = 41
        max_password = 'a' * max_length
        data = {'email': max_email, 'password': max_password}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_less_min_length_username(self):
        min_length = 3
        min_email = 'a' * min_length
        data = {'email': min_email, 'password': '123456'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_less_min_length_password(self):
        min_length = 5
        min_password = 'a' * min_length
        data = {'email': 'i@bilgin.top', 'password': min_password}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_less_min_length_username_password(self):
        min_length = 3
        min_email = 'a' * min_length
        min_length = 5
        min_password = 'a' * min_length
        data = {'email': min_email, 'password': min_password}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_correct_username_password(self):
        data = {'email': 'i@bilgin.top', 'password': '20020207yh'}
        response = self.app.post('/user/login', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class TestCaptcha(unittest.TestCase):

    """
    Total test cases: 8
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_empty_email_captcha(self):
        data = {'email': '', 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please deliver your e-mail first! ')

    def test_empty_email(self):
        data = {'email': '', 'captcha': '1234'}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Please deliver your e-mail first! ')

    def test_empty_captcha(self):
        data = {'email': '12345678@qq.com', 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)[1]['message'], 'Successfully send you email!')

    def test_correct_email_captcha(self):
        data = {'email': 'i@bilgin.top', 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)[1]['message'], 'Successfully send you email!')

    def test_wrong_email_captcha(self):
        data = {'email': 'test', 'captcha': '1234'}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Internal Server Error')

    def test_wrong_email(self):
        data = {'email': 'test', 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Internal Server Error')

    def test_exceed_max_length_email(self):
        max_length = 51
        max_email = 'a' * max_length + '@gmail.com'
        data = {'email': max_email, 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)[1]['message'], 'Successfully send you email!')

    def test_less_min_length_email(self):
        min_length = 3
        min_email = 'a' * min_length
        data = {'email': min_email, 'captcha': ''}
        response = self.app.post('/user/captcha', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(json.loads(response.data)['message'], 'Internal Server Error')


class TestRegister(unittest.TestCase):

    """
    Total test cases: 61
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_empty_email_username_password_captcha(self):
        data = {'email': '', 'username': '', 'password': '', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email(self):
        data = {'email': '', 'username': 'test', 'password': '123456', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username(self):
        data = {'email': 'test@123.com', 'username': '', 'password': '123456', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_password(self):
        data = {'email': 'test@123.com', 'username': 'test', 'password': '', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_captcha(self):
        data = {'email': 'test@123.com', 'username': 'test', 'password': '', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_username_password(self):
        data = {'email': '', 'username': '', 'password': '', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_username(self):
        data = {'email': '', 'username': '', 'password': '123456', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_password(self):
        data = {'email': '', 'username': 'test', 'password': '', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username_password(self):
        data = {'email': 'test@123.com', 'username': '', 'password': '', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_captcha(self):
        data = {'email': '', 'username': '', 'password': '123456', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username_captcha(self):
        data = {'email': 'test@123.com', 'username': '', 'password': '123456', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_password_captcha(self):
        data = {'email': 'test@123.com', 'username': 'test', 'password': '', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_username_capthca(self):
        data = {'email': '', 'username': '', 'password': '123456', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_email_password_captcha(self):
        data = {'email': '', 'username': 'test', 'password': '', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username_password_captcha(self):
        data = {'email': 'test@123.com', 'username': '', 'password': '', 'captcha': ''}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_email(self):
        data = {'email': 'test', 'username': 'test', 'password': '123456', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_captcha(self):
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_email_captcha(self):
        data = {'email': 'test', 'username': 'test', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_email(self):
        data = {'email': 'i@bilgin.top', 'username': 'test', 'password': '123456', 'captcha': '1234'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_username(self):
        data = {'email': 'test@bilgin.top', 'username': 'Bilgin', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_email_username(self):
        data = {'email': 'i@bilgin.top', 'username': 'Bilgin', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_email_captcha(self):
        data = {'email': 'i@bilgin.top', 'username': 'test', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_username_captcha(self):
        data = {'email': 'test@bilgin.top', 'username': 'Bilgin', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_existing_email_username_captcha(self):
        data = {'email': 'i@bilgin.top', 'username': 'Bilgin', 'password': '123456', 'captcha': '2345'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_email(self):
        data = {'email': 'test@', 'username': 'Bilgin', 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_username(self):
        data = {'email': 'test@bilgin.top', 'username': '[]:,.|', 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_captcha(self):
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': '', 'captcha': ';,|,'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_email_username(self):
        data = {'email': 'test@', 'username': '[]:,.|', 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_email_captcha(self):
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': '', 'captcha': ';,|,'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_username_captcha(self):
        data = {'email': 'test@bilgin.top', 'username': '[]:,.|', 'password':'123456', 'captcha': ';,|,'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_wrong_characters_email_username_captcha(self):
        data = {'email': 'test@', 'username': '[]:,.|', 'password': '', 'captcha': ';,|,'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_username(self):
        max_length = 21
        username = 'a' * max_length
        data = {'email': 'test@bilgin.top', 'username': username, 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email(self):
        max_length = 51
        email = 'a' * max_length
        data = {'email': email, 'username': 'test', 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_password(self):
        max_length = 41
        password = 'a' * max_length
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_captcha(self):
        max_length = 5
        captcha = 'a' * max_length
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_username(self):
        max_length_email = 51
        max_length_username = 21
        email = 'a' * max_length_email
        username = 'a' * max_length_username
        data = {'email': email, 'username': username, 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_password(self):
        max_length_email = 51
        max_length_password = 41
        email = 'a' * max_length_email
        password = 'a' * max_length_password
        data = {'email': email, 'username': 'test', 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_captcha(self):
        max_length_email = 51
        max_length_captcha = 5
        email = 'a' * max_length_email
        captcha = 'a' * max_length_captcha
        data = {'email': email, 'username': 'test', 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_username_password(self):
        max_length_username = 21
        max_length_password = 41
        username = 'a' * max_length_username
        password = 'a' * max_length_password
        data = {'email': 'test@bilgin.top', 'username': username, 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_username_captcha(self):
        max_length_username = 21
        max_length_captcha = 5
        username = 'a' * max_length_username
        captcha = 'a' * max_length_captcha
        data = {'email': 'test@bilgin.top', 'username': username, 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_password_captcha(self):
        max_length_password = 41
        max_length_captcha = 5
        password = 'a' * max_length_password
        captcha = 'a' * max_length_captcha
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)

    def test_max_length_email_username_password(self):
        max_length_email = 51
        max_length_username = 21
        max_length_password = 41
        email = 'a' * max_length_email
        username = 'a' * max_length_username
        password = 'a' * max_length_password
        data = {'email': email, 'username': username, 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_username_captcha(self):
        max_length_email = 51
        max_length_username = 21
        max_length_captcha = 5
        email = 'a' * max_length_email
        username = 'a' * max_length_username
        captcha = 'a' * max_length_captcha
        data = {'email': email, 'username': username, 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_password_captcha(self):
        max_length_email = 51
        max_length_password = 41
        max_length_captcha = 5
        email = 'a' * max_length_email
        password = 'a' * max_length_password
        captcha = 'a' * max_length_captcha
        data = {'email': email, 'username': 'test', 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_username_password_captcha(self):
        max_length_username = 21
        max_length_password = 41
        max_length_captcha = 5
        username = 'a' * max_length_username
        password = 'a' * max_length_password
        captcha = 'a' * max_length_captcha
        data = {'email': 'test@bilgin.top', 'username': username, 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_max_length_email_username_password_captcha(self):
        max_length_email = 51
        max_length_username = 21
        max_length_password = 41
        max_length_captcha = 5
        email = 'a' * max_length_email
        username = 'a' * max_length_username
        password = 'a' * max_length_password
        captcha = 'a' * max_length_captcha
        data = {'email': email, 'username': username, 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_username_password_captcha(self):
        min_length_email = 3
        min_length_username = 2
        min_length_password = 5
        min_length_captcha = 3
        email = 'a' * min_length_email
        username = 'a' * min_length_username
        password = 'a' * min_length_password
        captcha = 'a' * min_length_captcha
        data = {'email': email, 'username': username, 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_username_password(self):
        min_length_email = 3
        min_length_username = 2
        min_length_password = 5
        email = 'a' * min_length_email
        username = 'a' * min_length_username
        password = 'a' * min_length_password
        data = {'email': email, 'username': username, 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_username_captcha(self):
        min_length_email = 3
        min_length_username = 2
        min_length_captcha = 3
        email = 'a' * min_length_email
        username = 'a' * min_length_username
        captcha = 'a' * min_length_captcha
        data = {'email': email, 'username': username, 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_password_captcha(self):
        min_length_email = 3
        min_length_password = 5
        min_length_captcha = 3
        email = 'a' * min_length_email
        password = 'a' * min_length_password
        captcha = 'a' * min_length_captcha
        data = {'email': email, 'username': 'test', 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_username_password_captcha(self):
        min_length_username = 2
        min_length_password = 5
        min_length_captcha = 3
        username = 'a' * min_length_username
        password = 'a' * min_length_password
        captcha = 'a' * min_length_captcha
        data = {'email': 'test@bilgin.top', 'username': username, 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_username(self):
        min_length_email = 3
        min_length_username = 2
        email = 'a' * min_length_email
        username = 'a' * min_length_username
        data = {'email': email, 'username': username, 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_password(self):
        min_length_email = 3
        min_length_password = 5
        email = 'a' * min_length_email
        password = 'a' * min_length_password
        data = {'email': email, 'username': 'test', 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email_captcha(self):
        min_length_email = 3
        min_length_captcha = 3
        email = 'a' * min_length_email
        captcha = 'a' * min_length_captcha
        data = {'email': email, 'username': 'test', 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_username_password(self):
        min_length_username = 2
        min_length_password = 5
        username = 'a' * min_length_username
        password = 'a' * min_length_password
        data = {'email': 'test@bilgin.top', 'username': username, 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_username_captcha(self):
        min_length_username = 2
        min_length_captcha = 3
        username = 'a' * min_length_username
        captcha = 'a' * min_length_captcha
        data = {'email': 'test@bilgin.top', 'username': username, 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_password_captcha(self):
        min_length_password = 5
        min_length_captcha = 3
        password = 'a' * min_length_password
        captcha = 'a' * min_length_captcha
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': password, 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_email(self):
        min_length_email = 3
        email = 'a' * min_length_email
        data = {'email': email, 'username': 'test', 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_username(self):
        min_length_username = 2
        username = 'a' * min_length_username
        data = {'email': 'test@bilgin.top', 'username': username, 'password': '123456', 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_password(self):
        min_length_password = 5
        password = 'a' * min_length_password
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': password, 'captcha': '1235'}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_min_length_captcha(self):
        min_length_captcha = 3
        captcha = 'a' * min_length_captcha
        data = {'email': 'test@bilgin.top', 'username': 'test', 'password': '123456', 'captcha': captcha}
        response = self.app.post('/user/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class TestEditUsername(unittest.TestCase):

    """
    Total: 5
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
        data = {'new_name': 'zzzh'}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_username(self):
        data = {'new_name': ''}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'Please deliver your new name first! ')

    def test_min_length_username(self):
        min_length_username = 3
        username = 'a' * min_length_username
        data = {'new_name': username}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the name is too short! ')

    def test_max_length_username(self):
        max_length_username = 21
        username = 'a' * max_length_username
        data = {'new_name': username}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the name is too long! ')

    def test_username_exist(self):
        data = {'new_name': 'Bilgin'}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The name is already taken! ')

    def test_username_success(self):
        data = {'new_name': 'Bilgin2'}
        response = self.app.post('/user/edit_name', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')


class TestEditDescription(unittest.TestCase):

    """
    Total: 5
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
        data = {'new_description': 'i am iron man'}
        response = self.app.post('/user/edit_description', data=data)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_description(self):
        data = {'new_description': ''}
        response = self.app.post('/user/edit_description', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'Please deliver your new description first! ')

    def test_min_length_description(self):
        min_length_description = 3
        description = 'a' * min_length_description
        data = {'new_description': description}
        response = self.app.post('/user/edit_description', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the description is too short! ')

    def test_max_length_description(self):
        max_length_description = 201
        description = 'a' * max_length_description
        data = {'new_description': description}
        response = self.app.post('/user/edit_description', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the description is too long! ')

    def test_success_description(self):
        data = {'new_description': 'hhhhh'}
        response = self.app.post('/user/edit_description', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')


class TestUploadAvatar(unittest.TestCase):

    """
    Total: 4
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

    def test_upload_none_image(self):
        data = {'file': None}
        response = self.app.post('/user/upload_avatar', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'Please deliver your avatar first! ')

    def test_upload_not_image(self):
        # upload a pdf file in 'resources/test_pdf.pdf'
        file = open('resources/test_pdf.pdf', 'rb')
        data = {'file': (file, 'test_pdf.pdf')}
        response = self.app.post('/user/upload_avatar', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The format of the file is wrong! ')
        # close the file
        file.close()

    def test_upload_large_image(self):
        # upload a large image in 'resources/test_large_image.jpg'
        data = {'file': (open('resources/test_large.jpg', 'rb'), '4.png')}
        response = self.app.post('/user/upload_avatar', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The size of the file is too big! ')


class TestEditPassword(unittest.TestCase):

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
        data = {'captcha': '1234', 'password': '20020207yh', 'password_con': '20020207yh'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_empty_captcha(self):
        data = {'captcha': '', 'password': '20020207yh', 'password_con': '20020207yh'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The captcha is wrong! ')

    def test_wrong_captcha(self):
        data = {'captcha': '0000', 'password': '20020207yh', 'password_con': '20020207yh'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The captcha is wrong! ')

    def test_empty_password(self):
        data = {'captcha': '1234', 'password': '', 'password_con': '20020207yh'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the password is too short! ')

    def test_short_password(self):
        min_length_password = 5
        password = 'a' * min_length_password
        data = {'captcha': '1234', 'password': password, 'password_con': password}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the password is too short! ')

    def test_long_password(self):
        max_length_password = 21
        password = 'a' * max_length_password
        data = {'captcha': '1234', 'password': password, 'password_con': password}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the password is too long! ')

    def test_not_match_password(self):
        data = {'captcha': '1234', 'password': '20020207yh', 'password_con': '20020207yh1'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_empty_password_con(self):
        data = {'captcha': '1234', 'password': '2002020yh', 'password_con': ''}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_long_password_con(self):
        max_length_password = 21
        password = 'a' * max_length_password
        data = {'captcha': '1234', 'password': '20020207yh', 'password_con': password}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_short_password_con(self):
        min_length_password = 5
        password = 'a' * min_length_password
        data = {'captcha': '1234', 'password': '20020207yh', 'password_con': password}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_empty_capcha_password_con(self):
        data = {'captcha': '', 'password': '20020207yh', 'password_con': ''}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_wrong_captcha_password_con(self):
        data = {'captcha': '0000', 'password': '20020207yh', 'password_con': '20020207yh1'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_wrong_captcha_password(self):
        data = {'captcha': '0000', 'password': '20020207yh1', 'password_con': '20020207yh'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The password is not consistent! ')

    def test_empty_captcha_password(self):
        data = {'captcha': '', 'password': '', 'password_con': ''}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'The length of the password is too short! ')

    def test_correct_password(self):
        data = {'captcha': '1234', 'password': 'new_password', 'password_con': 'new_password'}
        response = self.app.post('/user/edit_password', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'You have changed your password successfully! ')


if __name__ == '__main__':
    unittest.main()
