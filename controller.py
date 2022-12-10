# from itsdangerous import TimedSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
# from config import SECRET_KEY
#
#
# # 生成token, 有效时间为600min
# def generate_auth_token(user_id, expiration=36000):
#     s = Serializer(SECRET_KEY, expires_in=expiration)
#     return s.dumps({'user_id': user_id})
from flask import session

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
        camp_user = CampUserModel.query.filter_by(user_id=user_id, identity="Member").all()
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

