# from itsdangerous import TimedSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
# from config import SECRET_KEY
#
#
# # 生成token, 有效时间为600min
# def generate_auth_token(user_id, expiration=36000):
#     s = Serializer(SECRET_KEY, expires_in=expiration)
#     return s.dumps({'user_id': user_id})
import datetime

from flask import session
from sqlalchemy import or_, extract
from datetime import timezone, timedelta

from models import CampUserModel, CampModel


# handle the string
# from {'captcha': ['Captcha Error! '], 'email': ['This email has been registered!']}
# to two sentences which can break a line in html
def handle_error_string(error):
    error_string = ""
    for key in error:
        error_string += error[key][0]
    return error_string


def get_all_camp_builder():
    user_id = session.get("user_id")
    if user_id:
        camp_user = CampUserModel.query.filter_by(user_id=user_id, identity="Builder").all()
        camps = []
        camp_dict = {}
        for camp in camp_user:
            camp_dict["camp_id"] = camp.camp_id
            camp = CampModel.query.filter_by(id=camp.camp_id).first()
            camp_dict["camp_name"] = camp.name
            camps.append(camp_dict)
            camp_dict = {}
        return camps
    else:
        return {}


def get_all_camp_join():
    user_id = session.get("user_id")
    if user_id:
        # get all camps which identity is "Member" and identity is "Admin"
        camp_user = CampUserModel.query.filter_by(user_id=user_id).filter(CampUserModel.identity.in_(["Admin", "Member"])).all()
        camps = []
        camp_dict = {}
        for camp in camp_user:
            camp_dict["camp_id"] = camp.camp_id
            camp = CampModel.query.filter_by(id=camp.camp_id).first()
            camp_dict["camp_name"] = camp.name
            camps.append(camp_dict)
            camp_dict = {}
        return camps
    else:
        return {}


def get_all_posts(post_model, camp_id,  order_by, category_id=None):

    # if the category_id is None, then get all posts
    if category_id is None:
        posts = post_model.query.filter_by(camp_id=camp_id, is_delete=0).order_by(post_model.is_top.desc())
    else:
        posts = post_model.query.filter_by(camp_id=camp_id, is_delete=0, category_id=category_id).order_by(post_model.is_top.desc())

    # sort the posts by the order_by
    if order_by == "new":
        posts = posts.order_by(post_model.update_time.desc())
    # elif order_by == "hot":
    #     posts = posts.order_by(post_model.like_count.desc())

    return posts


def save_all_notice_in_dict(post_model, camp_id):

    # get all posts which is not deleted in the camp
    posts = post_model.query.filter_by(camp_id=camp_id, is_delete=0, is_notice=1).all()

    notices = []
    notice_dict = {}
    for post in posts:
        notice_dict["post_id"] = post.id
        notice_dict["title"] = post.title
        notice_dict["category_id"] = post.category_id
        notice_dict["camp_id"] = post.camp_id
        notices.append(notice_dict)
        notice_dict = {}

    if len(notices) > 0:
        return notices
    else:
        return None


def save_all_posts_in_dict(post_model):

    posts = []
    post_dict = {}
    for post in post_model:
        post_dict["post_id"] = post.id
        post_dict["title"] = post.title
        post_dict["category_id"] = post.category_id
        post_dict["camp_id"] = post.camp_id
        post_dict["is_top"] = post.is_top
        post_dict["description"] = post.description
        post_dict["username"] = post.user.username
        post_dict["favorite_count"] = post.favorite_count
        post_dict["like_count"] = post.like_count
        post_dict["comment_count"] = post.comment_count
        posts.append(post_dict)
        post_dict = {}
    if len(posts) > 0:
        return posts
    else:
        return None
