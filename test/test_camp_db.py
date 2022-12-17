import unittest

from app import app
from extensions import db

from models import CampModel, CategoryModel, UserModel, CampUserModel, PostModel, FavoritePostModel, LikePostModel, CommentModel


class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

            # Create a camp
            camp = CampModel(name='test_camp', description='test_camp_description')
            db.session.add(camp)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_category_model(self):
        name = 'test_category'
        color = 'blue'

        with app.app_context():
            camp = CampModel.query.filter_by(name='test_camp').first()
            category = CategoryModel(name=name, color=color, camp_id=camp.id)

        with app.app_context():
            db.session.add(category)
            db.session.commit()
            category = CategoryModel.query.filter_by(name=name).first()

        self.assertEqual(category.name, name)
        self.assertEqual(category.color, color)
        self.assertEqual(category.camp_id, camp.id)

    def test_delete_category(self):
        name = 'test_category'
        color = 'blue'

        with app.app_context():
            camp = CampModel.query.filter_by(name='test_camp').first()
            category = CategoryModel(name=name, color=color, camp_id=camp.id)

        with app.app_context():
            db.session.add(category)
            db.session.commit()
            category = CategoryModel.query.filter_by(name=name).first()
            db.session.delete(category)
            db.session.commit()
            category = CategoryModel.query.filter_by(name=name).first()

        self.assertEqual(category, None)


class TestPostModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

            # Create a camp
            camp = CampModel(name='test_camp', description='test_camp_description')
            db.session.add(camp)
            db.session.commit()

            # Create a category
            category = CategoryModel(name='test_category', color='blue', camp_id=camp.id)
            db.session.add(category)
            db.session.commit()

            # Create a user
            user = UserModel(username='test_user',
                             password='test_password',
                             email='test_email@bilgin.top')
            db.session.add(user)
            db.session.commit()

            # Create a camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=user.id, identity='admin')
            db.session.add(camp_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_post_model(self):
        title = 'test_post'
        content = 'test_post_content'
        is_top = False
        is_notice = False
        is_delete = False
        description = 'test_post_description'
        favorite_count = 1
        like_count = 1
        comment_count = 1

        with app.app_context():
            camp = CampModel.query.filter_by(name='test_camp').first()
            category = CategoryModel.query.filter_by(name='test_category').first()
            user = UserModel.query.filter_by(username='test_user').first()
            camp_user = CampUserModel.query.filter_by(camp_id=camp.id, user_id=user.id).first()
            post = PostModel(title=title,
                             content=content,
                             is_top=is_top,
                             is_notice=is_notice,
                             is_delete=is_delete,
                             description=description,
                             favorite_count=favorite_count,
                             like_count=like_count,
                             comment_count=comment_count,
                             category_id=category.id,
                             user_id=user.id,
                             camp_id=camp.id)

        with app.app_context():
            db.session.add(post)
            db.session.commit()
            post = PostModel.query.filter_by(title=title).first()

        self.assertEqual(post.title, title)
        self.assertEqual(post.content, content)
        self.assertEqual(post.is_top, is_top)
        self.assertEqual(post.is_notice, is_notice)
        self.assertEqual(post.is_delete, is_delete)
        self.assertEqual(post.description, description)
        self.assertEqual(post.favorite_count, favorite_count)
        self.assertEqual(post.like_count, like_count)
        self.assertEqual(post.comment_count, comment_count)
        self.assertEqual(post.category_id, category.id)
        self.assertEqual(post.user_id, user.id)
        self.assertEqual(post.camp_id, camp.id)

    def test_delete_post(self):
        title = 'test_post'
        content = 'test_post_content'
        is_top = False
        is_notice = False
        is_delete = False
        description = 'test_post_description'
        favorite_count = 1
        like_count = 1
        comment_count = 1

        with app.app_context():
            camp = CampModel.query.filter_by(name='test_camp').first()
            category = CategoryModel.query.filter_by(name='test_category').first()
            user = UserModel.query.filter_by(username='test_user').first()
            camp_user = CampUserModel.query.filter_by(camp_id=camp.id, user_id=user.id).first()
            post = PostModel(title=title,
                             content=content,
                             is_top=is_top,
                             is_notice=is_notice,
                             is_delete=is_delete,
                             description=description,
                             favorite_count=favorite_count,
                             like_count=like_count,
                             comment_count=comment_count,
                             category_id=category.id,
                             user_id=user.id,
                             camp_id=camp.id)

        with app.app_context():
            db.session.add(post)
            db.session.commit()
            post = PostModel.query.filter_by(title=title).first()
            db.session.delete(post)
            db.session.commit()
            post = PostModel.query.filter_by(title=title).first()

        self.assertEqual(post, None)


class TestFavoriteModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

            # Create a camp
            camp = CampModel(name='test_camp', description='test_camp_description')
            db.session.add(camp)
            db.session.commit()

            # Create a category
            category = CategoryModel(name='test_category', color='blue', camp_id=camp.id)
            db.session.add(category)
            db.session.commit()

            # Create a user
            user = UserModel(username='test_user',
                             password='test_password',
                             email='test_db@bilgin.top')
            db.session.add(user)
            db.session.commit()

            # Create a camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=user.id, identity='admin')
            db.session.add(camp_user)
            db.session.commit()

            # Create a post
            post = PostModel(title='test_post',
                             content='test_post_content',
                             is_top=False,
                             is_notice=False,
                             is_delete=False,
                             description='test_post_description',
                             favorite_count=1,
                             like_count=1,
                             comment_count=1,
                             category_id=category.id,
                             user_id=user.id,
                             camp_id=camp.id)
            db.session.add(post)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_favorite_model(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            favorite = FavoritePostModel(user_id=user.id, post_id=post.id)

        with app.app_context():
            db.session.add(favorite)
            db.session.commit()
            favorite = FavoritePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(favorite.user_id, user.id)
        self.assertEqual(favorite.post_id, post.id)

    def test_delete_favorite(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            favorite = FavoritePostModel(user_id=user.id, post_id=post.id)

        with app.app_context():
            db.session.add(favorite)
            db.session.commit()
            favorite = FavoritePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()
            db.session.delete(favorite)
            db.session.commit()
            favorite = FavoritePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(favorite, None)


class TestLikeModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

            # Create a camp
            camp = CampModel(name='test_camp', description='test_camp_description')
            db.session.add(camp)
            db.session.commit()

            # Create a category
            category = CategoryModel(name='test_category', color='blue', camp_id=camp.id)
            db.session.add(category)
            db.session.commit()

            # Create a user
            user = UserModel(username='test_user',
                             password='test_password',
                             email='test_db@bilgin.top')
            db.session.add(user)
            db.session.commit()

            # Create a camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=user.id, identity='admin')
            db.session.add(camp_user)
            db.session.commit()

            # Create a post
            post = PostModel(title='test_post',
                             content='test_post_content',
                             is_top=False,
                             is_notice=False,
                             is_delete=False,
                             description='test_post_description',
                             favorite_count=1,
                             like_count=1,
                             comment_count=1,
                             category_id=category.id,
                             user_id=user.id,
                             camp_id=camp.id)

            db.session.add(post)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_like_model(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            like = LikePostModel(user_id=user.id, post_id=post.id)

        with app.app_context():
            db.session.add(like)
            db.session.commit()
            like = LikePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(like.user_id, user.id)
        self.assertEqual(like.post_id, post.id)

    def test_delete_like(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            like = LikePostModel(user_id=user.id, post_id=post.id)

        with app.app_context():
            db.session.add(like)
            db.session.commit()
            like = LikePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()
            db.session.delete(like)
            db.session.commit()
            like = LikePostModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(like, None)


class TestCommentModel(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.testing = True
            self.db_url = 'sqlite:///' + "test.db"
            app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
            self.app = app.test_client()
            db.create_all()

            # Create a camp
            camp = CampModel(name='test_camp', description='test_camp_description')
            db.session.add(camp)
            db.session.commit()

            # Create a category
            category = CategoryModel(name='test_category', color='blue', camp_id=camp.id)
            db.session.add(category)
            db.session.commit()

            # Create a user
            user = UserModel(username='test_user',
                             password='test_password',
                             email='test@bilgin.top')
            db.session.add(user)
            db.session.commit()

            # Create a camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=user.id, identity='admin')
            db.session.add(camp_user)
            db.session.commit()

            # Create a post
            post = PostModel(title='test_post',
                             content='test_post_content',
                             is_top=False,
                             is_notice=False,
                             is_delete=False,
                             description='test_post_description',
                             favorite_count=1,
                             like_count=1,
                             comment_count=1,
                             category_id=category.id,
                             user_id=user.id,
                             camp_id=camp.id)

            db.session.add(post)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_comment_model(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            comment = CommentModel(content='test_comment_content',
                                   user_id=user.id,
                                   post_id=post.id,
                                   is_delete=False)

        with app.app_context():
            db.session.add(comment)
            db.session.commit()
            comment = CommentModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(comment.user_id, user.id)
        self.assertEqual(comment.post_id, post.id)

    def test_delete_comment(self):
        with app.app_context():
            user = UserModel.query.filter_by(username='test_user').first()
            post = PostModel.query.filter_by(title='test_post').first()
            comment = CommentModel(content='test_comment_content',
                                   user_id=user.id,
                                   post_id=post.id,
                                   is_delete=False)

        with app.app_context():
            db.session.add(comment)
            db.session.commit()
            comment = CommentModel.query.filter_by(user_id=user.id, post_id=post.id).first()
            db.session.delete(comment)
            db.session.commit()
            comment = CommentModel.query.filter_by(user_id=user.id, post_id=post.id).first()

        self.assertEqual(comment, None)


if __name__ == '__main__':
    unittest.main()
