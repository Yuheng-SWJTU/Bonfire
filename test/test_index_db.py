import unittest

from sqlalchemy.orm import session, sessionmaker

from app import app
from extensions import db

from models import CampModel, CampUserModel, UserModel


class TestCampModel(unittest.TestCase):
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

    def test_camp_model(self):
        camp = CampModel(name='test_camp', description='test_camp_description')

        with app.app_context():
            db.session.add(camp)
            db.session.commit()
            camp = CampModel.query.filter_by(name='test_camp').first()

        self.assertEqual(camp.name, 'test_camp')
        self.assertEqual(camp.description, 'test_camp_description')
        self.assertEqual(camp.background, "default_camp.png")

    def test_camp_details_model(self):
        camp = CampModel(name='test_camp', description='test_camp_description', background="test_camp_background.png")

        with app.app_context():
            db.session.add(camp)
            db.session.commit()
            camp = CampModel.query.filter_by(name='test_camp').first()

        self.assertEqual(camp.name, 'test_camp')
        self.assertEqual(camp.description, 'test_camp_description')
        self.assertEqual(camp.background, "test_camp_background.png")

    def test_delete_camp(self):
        camp = CampModel(name='test_camp', description='test_camp_description')

        with app.app_context():
            db.session.add(camp)
            db.session.commit()
            camp = CampModel.query.filter_by(name='test_camp').first()
            db.session.delete(camp)
            db.session.commit()
            camp = CampModel.query.filter_by(name='test_camp').first()

        self.assertEqual(camp, None)


class TestCampUserModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            session.expire_on_commit = False
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()
            sessionmaker(expire_on_commit=False)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_camp_user_model(self):
        user = UserModel(username='test_user', email='test_db@bilgin.top', password='123456')
        camp = CampModel(name='test_camp', description='test_camp_description')

        with app.app_context():
            db.session.add(user)
            db.session.add(camp)
            db.session.commit()

            camp_user = CampUserModel(user_id=user.id, camp_id=camp.id, identity='admin')

            db.session.add(camp_user)
            db.session.commit()
            camp_user = CampUserModel.query.filter_by(user_id=user.id).first()

        self.assertEqual(camp_user.user_id, 1)
        self.assertEqual(camp_user.camp_id, 1)
        self.assertEqual(camp_user.identity, 'admin')


if __name__ == '__main__':
    unittest.main()
