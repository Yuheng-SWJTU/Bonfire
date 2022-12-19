# ///////////////////////////////////////////////////////////////////////////
# import wtforms
import wtforms
from wtforms.validators import length, email
# import models
from models import EmailCaptchaModel, UserModel, ChangePasswordCaptchaModel, CampModel, CategoryModel
from flask import g
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


class ChangePassword(wtforms.Form):
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=40)])
    password_con = wtforms.StringField(validators=[length(min=6, max=40)])

    def validate_captcha(self, field):
        captcha = field.data
        email = g.user.email
        captcha_model = ChangePasswordCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha != captcha:
            raise wtforms.ValidationError("Captcha Error! ")

    def validate_password_con(self, field):
        password = self.password.data
        password_con = field.data
        if password != password_con:
            raise wtforms.ValidationError("Password not match! ")


class BuildCampForm(wtforms.Form):
    """
    When user build a camp, the form will be sent to this validator.
    """

    camp_name = wtforms.StringField(validators=[length(min=1, max=20)])
    description = wtforms.StringField(validators=[length(min=1, max=200)])

    def check_name(self, field):
        camp_name = field.data
        camp_model = CampModel.query.filter_by(name=camp_name).first()
        if camp_model:
            raise wtforms.ValidationError("This camp name has been used!")


class AddCategoryForm(wtforms.Form):
    """
    When user add a category, the form will be sent to this validator.

    """

    category_name = wtforms.StringField(validators=[length(min=1, max=20)])

    def check_name(self, field):
        category_name = field.data
        category_model = CategoryModel.query.filter_by(name=category_name).first()
        if category_model:
            raise wtforms.ValidationError("This category name has been used!")


class AddPostForm(wtforms.Form):
    """
    When user add a post, the form will be sent to this validator.
    """

    post_title = wtforms.StringField(validators=[length(min=1, max=20)])
    post_content = wtforms.StringField(validators=[length(min=1, max=1000)])

    def check_title_length(self, field):
        post_title = field.data
        if len(post_title) > 20:
            raise wtforms.ValidationError("The length of title should be less than 20!")

    def check_content_length(self, field):
        post_content = field.data
        if len(post_content) > 1000:
            raise wtforms.ValidationError("The length of content should be less than 1000!")


class CommentForm(wtforms.Form):
    """
    When user add a comment, the form will be sent to this validator.
    """

    comment_content = wtforms.StringField(validators=[length(min=1, max=1000)])

    def check_content_length(self, field):
        comment_content = field.data
        if len(comment_content) > 200:
            raise wtforms.ValidationError("The length of comment should be less than 200!")
        if len(comment_content) < 1:
            raise wtforms.ValidationError("The length of comment should be more than 1!")


class SearchForm(wtforms.Form):
    """
    When user search, the form will be sent to this validator.、

    """

    search_content = wtforms.StringField(validators=[length(min=1, max=20)])

    def check_content_length(self, field):
        search_content = field.data
        if len(search_content) > 20:
            raise wtforms.ValidationError("The length of search should be less than 20!")
        if len(search_content) < 1:
            raise wtforms.ValidationError("The length of search should be more than 1!")


class ChangeProfileForm(wtforms.Form):
    """
    When user change profile, the form will be sent to this validator.

    """

    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    description = wtforms.StringField(validators=[length(min=1, max=200)])

    def validate_username(self, field):
        username = field.data
        user_model = UserModel.query.filter_by(username=username).first()
        if user_model and user_model.id != g.user.id:
            raise wtforms.ValidationError("This username has been registered!")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model and user_model.id != g.user.id:
            raise wtforms.ValidationError("This email has been registered!")

    def validate_description(self, field):
        description = field.data
        if len(description) > 200:
            raise wtforms.ValidationError("The length of description should be less than 200!")
        if len(description) < 1:
            raise wtforms.ValidationError("The length of description should be more than 1!")


class ChangeCampForm(wtforms.Form):
    """
    When user change camp, the form will be sent to this validator.
    """

    camp_name = wtforms.StringField(validators=[length(min=1, max=20)])
    description = wtforms.StringField(validators=[length(min=1, max=200)])

    def check_name(self, field):
        camp_name = field.data
        camp_model = CampModel.query.filter_by(name=camp_name).first()
        if camp_model and camp_model.id != g.camp.id:
            raise wtforms.ValidationError("This camp name has been used!")

    def check_description(self, field):
        description = field.data
        if len(description) > 200:
            raise wtforms.ValidationError("The length of description should be less than 200!")
        if len(description) < 1:
            raise wtforms.ValidationError("The length of description should be more than 1!")


class ChangeCategoryForm(wtforms.Form):
    """
    When user change category, the form will be sent to this validator.
    """

    category_name = wtforms.StringField(validators=[length(min=1, max=20)])

    def check_name(self, field):
        category_name = field.data
        category_model = CategoryModel.query.filter_by(name=category_name).first()
        if category_model and category_model.id != g.category.id:
            raise wtforms.ValidationError("This category name has been used!")


class ChangePostForm(wtforms.Form):
    """
    When user change post, the form will be sent to this validator.
    """

    post_title = wtforms.StringField(validators=[length(min=1, max=20)])
    post_content = wtforms.StringField(validators=[length(min=1, max=1000)])

    def check_title_length(self, field):
        post_title = field.data
        if len(post_title) > 20:
            raise wtforms.ValidationError("The length of title should be less than 20!")

    def check_content_length(self, field):
        post_content = field.data
        if len(post_content) > 1000:
            raise wtforms.ValidationError("The length of content should be less than 1000!")


class ChangePasswordForm(wtforms.Form):
    """
    When user change password, the form will be sent to this validator.
    """

    old_password = wtforms.PasswordField(validators=[length(min=6, max=20)])
    new_password = wtforms.PasswordField(validators=[length(min=6, max=20)])
    new_password_again = wtforms.PasswordField(validators=[length(min=6, max=20)])

    def validate_old_password(self, field):
        old_password = field.data
        if not g.user.check_password(old_password):
            raise wtforms.ValidationError("The old password is wrong!")

    def validate_new_password(self, field):
        new_password = field.data
        if len(new_password) < 6:
            raise wtforms.ValidationError("The length of new password should be more than 6!")
        if len(new_password) > 20:
            raise wtforms.ValidationError("The length of new password should be less than 20!")

    def validate_new_password_again(self, field):
        new_password = self.new_password.data
        new_password_again = field.data
        if new_password != new_password_again:
            raise wtforms.ValidationError("The new password is not the same!")


class ChangeUsernameForm(wtforms.Form):
    """
    When user change username, the form will be sent to this validator.

    """

    username = wtforms.StringField(validators=[length(min=1, max=20)])
    password = wtforms.PasswordField(validators=[length(min=6, max=20)])

    def validate_username(self, field):
        username = field.data
        user_model = UserModel.query.filter_by(username=username).first()
        if user_model and user_model.id != g.user.id:
            raise wtforms.ValidationError("This username has been registered!")

    def validate_password(self, field):
        password = field.data
        if not g.user.check_password(password):
            raise wtforms.ValidationError("The password is wrong!")
