# ///////////////////////////////////////////////////////////////////////////
from extensions import db
from datetime import datetime
# ///////////////////////////////////////////////////////////////////////////


class EmailCaptchaModel(db.Model):
    """
    This class is used to store email captcha.

    """

    __tablename__ = "email_captcha"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


class ChangePasswordCaptchaModel(db.Model):
    __tablename__ = "change_password_captcha"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    """
    This class is used to store user information.

    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), nullable=False, default="default.png")
    gender = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class CampModel(db.Model):
    """
    This class is used to store camp information.

    """

    __tablename__ = "camp"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    description = db.Column(db.String(200), nullable=True)
    background = db.Column(db.String(200), nullable=True, default="default_camp.png")
    create_time = db.Column(db.DateTime, default=datetime.now)


class CampUserModel(db.Model):
    """
    This class is used to store camp user information.

    """

    __tablename__ = "camp_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    identity = db.Column(db.String(100), nullable=False, unique=False)

    # User id will be the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Camp id will be the foreign key
    camp_id = db.Column(db.Integer, db.ForeignKey("camp.id"))

    # if you want to get all the camps of a user, you can write it through camps
    user = db.relationship("UserModel", backref="camps")
    # if you want to get all the users of a camp, you can write it through users
    camp = db.relationship("CampModel", backref="users")


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    color = db.Column(db.String(100), nullable=False, unique=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # Camp id will be the foreign key
    camp_id = db.Column(db.Integer, db.ForeignKey("camp.id"))
    # if you want to get all the categories of a camp, you can write it through categories
    camp = db.relationship("CampModel", backref="categories")


class PostModel(db.Model):
    """
    This class is used to store post information.

    """

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    is_top = db.Column(db.Boolean, default=False)
    is_notice = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200), nullable=True)
    favorite_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)

    # User id will be the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Camp id will be the foreign key
    camp_id = db.Column(db.Integer, db.ForeignKey("camp.id"))
    # Category id will be the foreign key
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    # if you want to get all the posts of a user, you can write it through posts
    user = db.relationship("UserModel", backref="posts")
    # if you want to get all the posts of a camp, you can write it through posts
    camp = db.relationship("CampModel", backref="posts")
    # if you want to get all the posts of a category, you can write it through posts
    category = db.relationship("CategoryModel", backref="posts")


class FavoritePostModel(db.Model):
    """
    This class is used to store favorite post information.

    """

    __tablename__ = "favorite_post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # User id will be the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Post id will be the foreign key
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    # if you want to get all the favorite posts of a user, you can write it through favorite_posts
    user = db.relationship("UserModel", backref="favorite_posts")
    # if you want to get all the favorite users of a post, you can write it through favorite_users
    post = db.relationship("PostModel", backref="favorite_users")
