import unittest
from app import app
from extensions import db

from models import EmailCaptchaModel, ChangePasswordCaptchaModel, UserModel


class TestEmailCaptchaModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_email_captcha_model(self):
        email = 'test_db@bilgin.top'
        captcha = '1234'
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)

        with app.app_context():
            db.session.add(email_captcha)
            db.session.commit()
            email_captcha = EmailCaptchaModel.query.filter_by(email=email).first()

        self.assertEqual(email_captcha.email, email)
        self.assertEqual(email_captcha.captcha, captcha)


class TestChangePasswordCaptchaModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_change_password_captcha_model(self):
        email = 'test_db@bilgin.top'
        captcha = '1234'
        change_password_captcha = ChangePasswordCaptchaModel(email=email, captcha=captcha, user_id=1)

        with app.app_context():
            db.session.add(change_password_captcha)
            db.session.commit()
            change_password_captcha = ChangePasswordCaptchaModel.query.filter_by(email=email).first()

        self.assertEqual(change_password_captcha.email, email)
        self.assertEqual(change_password_captcha.captcha, captcha)
        self.assertEqual(change_password_captcha.user_id, 1)


class TestUserModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model(self):
        username = 'test_db'
        email = 'test_db@bilgin.top'
        password = '123456'
        user = UserModel(username=username, email=email, password=password)

        with app.app_context():
            db.session.add(user)
            db.session.commit()
            user = UserModel.query.filter_by(email=email).first()

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)

    def test_user_details_model(self):
        username = 'test_db'
        email = 'test_db@bilgin.top'
        password = '123456'
        avatar = 'test.png'
        gender = 'Male'
        description = 'test'
        email_inform = True
        user = UserModel(username=username, email=email, password=password, avatar=avatar, description=description,
                         gender=gender, email_inform=email_inform)

        with app.app_context():
            db.session.add(user)
            db.session.commit()
            user = UserModel.query.filter_by(email=email).first()

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)
        self.assertEqual(user.avatar, avatar)
        self.assertEqual(user.gender, gender)
        self.assertEqual(user.description, description)
        self.assertEqual(user.email_inform, email_inform)

    def test_delete_user(self):
        username = 'test_db'
        email = 'test_db@bilgin.top'
        password = '123456'
        user = UserModel(username=username, email=email, password=password)

        with app.app_context():
            db.session.add(user)
            db.session.commit()
            user = UserModel.query.filter_by(email=email).first()
            db.session.delete(user)
            db.session.commit()
            user = UserModel.query.filter_by(email=email).first()

        self.assertEqual(user, None)


if __name__ == '__main__':
    unittest.main()
