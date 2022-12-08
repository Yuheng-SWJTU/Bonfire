# from itsdangerous import TimedSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
# from config import SECRET_KEY
#
#
# # 生成token, 有效时间为600min
# def generate_auth_token(user_id, expiration=36000):
#     s = Serializer(SECRET_KEY, expires_in=expiration)
#     return s.dumps({'user_id': user_id})


# handle the string
# from {'captcha': ['Captcha Error! '], 'email': ['This email has been registered!']}
# to two sentences which can break a line in html
def handle_error_string(error):
    error_string = ""
    for key in error:
        error_string += error[key][0]
    return error_string

