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

