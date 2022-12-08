# ///////////////////////////////////////////////////////////////////////////
# import wtforms
import wtforms
from wtforms.validators import length, email
# import models
from models import EmailCaptchaModel, UserModel
from flask import session
# ///////////////////////////////////////////////////////////////////////////


class RegisterForm(wtforms.Form):
    """
    When user register, the form will be sent to this validator.

    username - the length of username should be between 3 and 20
    email - the format of email should be correct
    captcha - the length of captcha should be 4
    password - the length of password should be between 6 and 40

    """

    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=40)])

    # Check whether captcha correct
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha != captcha:
            raise wtforms.ValidationError("Captcha Error! ")

    # Check whether email exit
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("This email has been registered!")


    def validate_username(self, field):
        username = field.data
        user_model = UserModel.query.filter_by(username=username).first()
        if user_model:
            raise wtforms.ValidationError("This username has been registered!")


class LoginForm(wtforms.Form):
    """
    When user login, the form will be sent to this validator.

    email - the format of email should be correct
    password - the length of password should be between 6 and 40

    """

    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=40)])
