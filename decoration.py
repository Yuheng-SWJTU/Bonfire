from models import CategoryModel, CampModel, CampUserModel, PostModel, UserModel

from flask import session
from flask_mail import Message
from flask import g, redirect, url_for
from extensions import db, mail
import datetime
from functools import wraps


def login_required(func):
    """
    This function is used to check whether the user is logged in.

    :param func: The function to be decorated
    :return: The decorated function

    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))

    return wrapper


def check_category(func):
    """
    This function is used to check whether the category is empty.

    :param func: The function to be decorated
    :return: The decorated function

    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        camp_id = session.get('camp_id')
        # Get a category id which name is 'Default' to the camp
        category = CategoryModel.query.filter_by(name="Default", camp_id=camp_id).first()

        # If the category is not exist, create a new category
        if not category:
            category = CategoryModel(name="Default", color="blue", camp_id=camp_id)
            db.session.add(category)
            db.session.commit()

        # Traverse all posts of the camp
        posts = PostModel.query.filter_by(camp_id=camp_id).all()

        # if there is a post without category, then redirect add a category called 'Default' to this post
        for post in posts:
            if not post.category:
                post.category = category
                db.session.commit()

        return func(*args, **kwargs)

    return wrapper
