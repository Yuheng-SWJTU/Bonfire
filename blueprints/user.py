import json
import os
import random
import string
from datetime import datetime
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from controller import handle_error_string, get_all_camp_builder, get_all_camp_join, get_user_ip

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response, current_app
from flask_mail import Message
from models import UserModel, EmailCaptchaModel, ChangePasswordCaptchaModel, FavoritePostModel, PostModel, LikePostModel
from extensions import db, mail
from .form import RegisterForm, LoginForm, ChangePassword
from werkzeug.security import generate_password_hash, check_password_hash

from config import AVATAR_UPLOAD_FOLDER

from decoration import login_required

# the information of the blueprint
bp = Blueprint("user", __name__, url_prefix="/user")
api = Api(bp)


@api.representation('text/html')
def output_html(data, code, headers=None):
    if isinstance(data, str):
        resp = Response(data)
        return resp
    else:
        return Response(json.dumps(data), mimetype='application/json')


class Login(Resource):
    """
    show the login page

    """

    def get(self):
        current_app.logger.info("IP: {} is trying to log in.".format(get_user_ip()))
        return render_template("login.html")

    def post(self):
        # form validation
        form = LoginForm(request.form)
        if form.validate():
            # get the form data
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                # save in session
                session['user_id'] = user.id
                session['sort'] = "popularity"
                session["user_name"] = user.username
                # remember me
                rememberme = request.form.getlist("remember")
                if "rememberme" in rememberme:
                    session['remember'] = "true"
                else:
                    session['remember'] = "false"
                current_app.logger.info("IP: {}, USERNAME: {} logged in.".format(get_user_ip(), user.username))
                return redirect("/")
            else:
                current_app.logger.info("IP: {} failed to log in.".format(get_user_ip()))
                return render_template("login.html", error="Email or password error!")
        else:
            current_app.logger.info("IP: {} failed to log in.".format(get_user_ip()))
            flash("The format of email or password is wrong! ")
            return redirect(url_for("user.login"))


class Register(Resource):
    """
    show the register page

    """

    def get(self):
        current_app.logger.info("IP: {} is trying to register.".format(get_user_ip()))
        return render_template("register.html")

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            # get the form data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # encrypt
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)

            # database rollback
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                current_app.logger.info("IP: {} failed to register.".format(get_user_ip()))
                return redirect(url_for("user.register"))
            current_app.logger.info("IP: {}, USERNAME: {} registered.".format(get_user_ip(), username))
            return redirect(url_for("user.login"))
        else:
            # get the error message form and handle it from json to string
            flash(handle_error_string(form.errors))
            # flash(form.errors)
            current_app.logger.info("IP: {} failed to register.".format(get_user_ip()))
            return redirect(url_for("user.register"))


class GetCaptcha(Resource):
    """
    get the captcha
    """

    def post(self):
        # GET request
        email = request.form.get("email")
        name = request.form.get("username")
        if name == "":
            name = "user"

        # generate the captcha
        letters = string.digits
        captcha = "".join(random.sample(letters, 4))

        # send the email
        if email:
            message = Message(
                subject="[Bonfire] - your register code",
                recipients=[email],
                body=f"Hi, {name} ! \n\n"
                     f"You can enter this code to register into Bonfire: \n\n"
                     f"{captcha} \n\n"
                     f"If you weren't trying to register in, let me know."
            )
            mail.send(message)

            # save the captcha in the session
            captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.captcha = captcha
                captcha_model.creat_time = datetime.now()

                # database rollback
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise e
            else:
                captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
                db.session.add(captcha_model)
                db.session.commit()
            current_app.logger.info("IP: {} gets a captcha.".format(get_user_ip()))
            return jsonify({"code": 200}, {"message": "Successfully send you email!"})
        else:
            current_app.logger.info("IP: {} failed to get a captcha.".format(get_user_ip()))
            return jsonify({"code": 400, "message": "Please deliver your e-mail first! "})


class Profile(Resource):
    """
    show the profile page

    """

    method_decorators = [login_required]

    def get(self):
        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        # get the latest post i created
        latest_post = PostModel.query.filter_by(user_id=g.user.id, is_delete=0).order_by(PostModel.create_time.desc()).first()
        if latest_post:
            latest_post = latest_post
        else:
            latest_post = None

        try:
            return render_template("profile.html", user=g.user, birthday=g.user.birthday.strftime("%Y-%m-%d"),
                                   status="profile", camp_builders=camp_builders, camp_joins=camp_joins, latest_post=latest_post)
        except Exception as e:
            current_app.logger.info("IP: {} failed to get profile. {}".format(get_user_ip(), e))
            return render_template("profile.html", user=g.user,
                                   status="profile", camp_builders=camp_builders, camp_joins=camp_joins, latest_post=latest_post)


class EditName(Resource):
    """
    edit the username

    """

    method_decorators = [login_required]

    def post(self):
        new_name = request.form.get("new_name")
        if new_name:
            # check the validation of the name
            if len(new_name) > 20:
                current_app.logger.info("{}[{}] failed to edit name, because the length of the name is too long.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The length of the name is too long! "})
            if len(new_name) < 4:
                current_app.logger.info("{}[{}] failed to edit name, because the length of the name is too short.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The length of the name is too short! "})

            # check the name is unique
            user = UserModel.query.filter_by(username=new_name).first()
            if user:
                current_app.logger.info("{}[{}] failed to edit name, because the name is already exist.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The name is already taken! "})

            # update the name in the database
            user_id = session.get("user_id")
            user = UserModel.query.filter_by(id=user_id).first()
            user.username = new_name
            # database rollback
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            current_app.logger.info("{}[{}] edited name.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 200})
        else:
            current_app.logger.info("{}[{}] failed to edit name, because the name is empty.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "Please deliver your new name first! "})


class EditDescription(Resource):
    """
    edit the description

    """

    method_decorators = [login_required]

    def post(self):
        new_description = request.form.get("new_description")
        if new_description:
            # check the validation of the description
            if len(new_description) > 200:
                current_app.logger.info("{}[{}] failed to edit description, because the length of the description is "
                                        "too long.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The length of the description is too long! "})

            if len(new_description) < 4:
                current_app.logger.info("{}[{}] failed to edit description, because the length of the description is "
                                        "too short.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The length of the description is too short! "})

            # update the description in the database
            user_id = session.get("user_id")
            user = UserModel.query.filter_by(id=user_id).first()
            user.description = new_description
            # database rollback
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.info("{}[{}] failed to edit description, because the database error.".format(session.get("user_name"), get_user_ip()))
                db.session.rollback()
                raise e
            current_app.logger.info("{}[{}] edited description.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 200})
        else:
            current_app.logger.info("{}[{}] failed to edit description, because the description is empty.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "Please deliver your new description first! "})


class EditProfile(Resource):
    """
    edit the profile

    """

    method_decorators = [login_required]

    def post(self):
        # get the form data
        gender = request.form.get("gender")
        birthday = request.form.get("birthday")
        # convert the date format from "2022-12-10" to "2022-12-10 00:00:00"
        birthday = datetime.strptime(birthday, "%Y-%m-%d")
        # Save the data in the database
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        user.gender = gender
        user.birthday = birthday
        # database rollback
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.info("{}[{}] failed to edit profile, because the database error.".format(session.get("user_name"), get_user_ip()))
            db.session.rollback()
            raise e
        current_app.logger.info("{}[{}] edited profile.".format(session.get("user_name"), get_user_ip()))
        return redirect(url_for("user.profile"))


class UploadAvatar(Resource):
    """
    upload the avatar

    """

    method_decorators = [login_required]

    def post(self):
        # get the file from layui upload component
        file = request.files.get("file")
        if file:
            # check the file format
            if file.filename.split(".")[-1] not in ["jpg", "png", "jpeg"]:
                current_app.logger.info("{}[{}] failed to upload avatar, because the file format is not supported.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The format of the file is wrong! "})
            # check the file size
            # print(len(file.read()) / 1024 / 1024)
            if len(file.read()) > 1024 * 1024 * 2:
                current_app.logger.info("{}[{}] failed to upload avatar, because the file size is too large.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The size of the file is too big! "})

            # before upload the file, delete the old file
            user_id = session.get("user_id")
            user = UserModel.query.filter_by(id=user_id).first()
            if user.avatar != "default.png":
                os.remove(os.path.join(AVATAR_UPLOAD_FOLDER, user.avatar))

            # save the file
            # change the file name into user_id + file format
            file_name = str(session.get("user_id")) + "." + file.filename.split(".")[-1]
            file_name = secure_filename(file_name)
            file.save(os.path.join(AVATAR_UPLOAD_FOLDER, file_name))
            # save the file name in the database
            user_id = session.get("user_id")
            user = UserModel.query.filter_by(id=user_id).first()
            user.avatar = file_name
            # database rollback
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.info("{}[{}] failed to upload avatar, because the database error.".format(session.get("user_name"), get_user_ip()))
                db.session.rollback()
                raise e
            current_app.logger.info("{}[{}] uploaded avatar.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 0})
        else:
            current_app.logger.info("{}[{}] failed to upload avatar, because the file is empty.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "Please deliver your avatar first! "})


class Privacy(Resource):
    """
    edit the privacy

    """

    method_decorators = [login_required]

    def get(self):
        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()
        # get the user information in the database
        user_id = session.get("user_id")
        user = UserModel.query.filter_by(id=user_id).first()
        return render_template("privacy.html", user=g.user,
                               status="privacy", camp_builders=camp_builders, camp_joins=camp_joins, user_info=user)


class GetChangePasswordCaptcha(Resource):
    """
    get the captcha of change password

    """

    method_decorators = [login_required]

    def post(self):
        # GET request
        email = g.user.email

        # generate the captcha
        letters = string.digits
        captcha = "".join(random.sample(letters, 4))

        # send the email
        if email:
            message = Message(
                subject="[Bonfire] - you are changing your password",
                recipients=[email],
                body=f"Hi, {g.user.username} ! \n\n"
                     f"You are changing your password: \n\n"
                     f"Please enter this captcha code to confirm \n\n"
                     f"{captcha} \n\n"
                     f"If you didn't change your password, please ignore this email. \n\n"
            )
            mail.send(message)

            # save the captcha in the session
            captcha_model = ChangePasswordCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.email = email
                captcha_model.user_id = g.user.id
                captcha_model.captcha = captcha
                captcha_model.creat_time = datetime.now()

                # database rollback
                try:
                    db.session.commit()
                except Exception as e:
                    current_app.logger.info("{}[{}] failed to get change password captcha, because the database error.".format(session.get("user_name"), get_user_ip()))
                    db.session.rollback()
                    raise e
            else:
                captcha_model = ChangePasswordCaptchaModel(email=email, captcha=captcha, user_id=g.user.id,
                                                           creat_time=datetime.now())
                db.session.add(captcha_model)
                db.session.commit()
            current_app.logger.info("{}[{}] requested change password captcha.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 200})
        else:
            current_app.logger.info("{}[{}] failed to request change password captcha, because the email is empty.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "We cannot detect your email address! "})


class EditPassword(Resource):
    """
    edit the password

    """

    method_decorators = [login_required]

    def post(self):
        captcha = request.form.get("captcha")
        password = request.form.get("password")
        password_con = request.form.get("password_con")

        # check the validation of the password
        if len(password) < 6:
            current_app.logger.info("{}[{}] failed to change password, because the password is too short.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "The length of the password is too short! "})

        if len(password) > 20:
            current_app.logger.info("{}[{}] failed to change password, because the password is too long.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "The length of the password is too long! "})

        if password != password_con:
            current_app.logger.info("{}[{}] failed to change password, because the password is not consistent.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "The password is not consistent! "})

        # Use form validation to check the captcha
        form = ChangePassword(request.form)
        if form.validate():
            # check the captcha
            captcha_model = ChangePasswordCaptchaModel.query.filter_by(email=g.user.email).first()
            if captcha_model.captcha == captcha:
                # update the password in the database
                user = UserModel.query.filter_by(id=g.user.id).first()
                user.password = generate_password_hash(password)
                # database rollback
                try:
                    db.session.commit()
                except Exception as e:
                    current_app.logger.info("{}[{}] failed to change password, because the database error.".format(session.get("user_name"), get_user_ip()))
                    db.session.rollback()
                    raise e
                current_app.logger.info("{}[{}] changed password.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 200, "message": "You have changed your password successfully! "})
            else:
                current_app.logger.info("{}[{}] failed to change password, because the captcha is wrong.".format(session.get("user_name"), get_user_ip()))
                return jsonify({"code": 400, "message": "The captcha is wrong! "})
        else:
            current_app.logger.info("{}[{}] failed to change password, because the captcha is wrong.".format(session.get("user_name"), get_user_ip()))
            return jsonify({"code": 400, "message": "The captcha is wrong! "})


class DeleteAccount(Resource):
    """
    delete the account

    """

    method_decorators = [login_required]

    def delete(self):
        # delete the user in the database
        user = UserModel.query.filter_by(id=g.user.id).first()
        # change the username to "Cancelled"
        user.username = "Cancelled"
        # change the email to "Cancelled"
        user.email = "Cancelled"
        # change the password to "Cancelled"
        user.password = "Cancelled"

        # delete the avatar in the folder
        if user.avatar != "default.png":
            os.remove(os.path.join(AVATAR_UPLOAD_FOLDER, user.avatar))

        # change the avatar to "default.png"
        user.avatar = "default.png"
        # database rollback
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.info("{}[{}] failed to delete account, because the database error.".format(session.get("user_name"), get_user_ip()))
            db.session.rollback()
            raise e
        session.clear()
        current_app.logger.warning("{}[{}] deleted account.".format(session.get("user_name"), get_user_ip()))
        return jsonify({"code": 200, "message": "You have deleted your account successfully! "})


class Logout(Resource):
    """
    logout

    """

    method_decorators = [login_required]

    def get(self):
        # delete the session
        session.clear()
        current_app.logger.info("{}[{}] logged out.".format(session.get("user_name"), get_user_ip()))
        return redirect(url_for("user.login"))


class FavoriteContent(Resource):
    """
    favorite the content

    """

    method_decorators = [login_required]

    def get(self):
        favorite_contents = FavoritePostModel.query.filter_by(user_id=g.user.id).all()
        # get all posts information
        posts = []
        post = {}
        for favorite_content in favorite_contents:
            post_model = PostModel.query.filter_by(id=favorite_content.post_id, is_delete=0).first()
            try:
                post["title"] = post_model.title
                post["description"] = post_model.description
                post["like_count"] = post_model.like_count
                post["comment_count"] = post_model.comment_count
                post["favorite_count"] = post_model.favorite_count
                post["camp_id"] = post_model.camp_id
                post["category_id"] = post_model.category_id
                post["post_id"] = post_model.id
                posts.append(post)
                post = {}
            except Exception as e:
                print(e)
                continue

        if len(posts) == 0:
            posts = None

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        return render_template("lists.html", status="favorite", posts=posts, user=g.user, camp_builders=camp_builders, camp_joins=camp_joins)


class LikeContent(Resource):
    """
    like the content

    """

    method_decorators = [login_required]

    def get(self):
        like_contents = LikePostModel.query.filter_by(user_id=g.user.id).all()
        # get all posts information
        posts = []
        post = {}
        for like_content in like_contents:
            post_model = PostModel.query.filter_by(id=like_content.post_id, is_delete=0).first()
            try:
                post["title"] = post_model.title
                post["description"] = post_model.description
                post["like_count"] = post_model.like_count
                post["comment_count"] = post_model.comment_count
                post["favorite_count"] = post_model.favorite_count
                post["camp_id"] = post_model.camp_id
                post["category_id"] = post_model.category_id
                post["post_id"] = post_model.id
                posts.append(post)
                post = {}
            except Exception as e:
                print(e)
                continue

        if len(posts) == 0:
            posts = None

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        return render_template("lists.html", status="like", posts=posts, user=g.user, camp_builders=camp_builders, camp_joins=camp_joins)


class MyPost(Resource):
    """
    my post

    """

    method_decorators = [login_required]

    def get(self):
        # get all posts information
        posts = []
        post = {}
        post_models = PostModel.query.filter_by(user_id=g.user.id, is_delete=0).all()
        for post_model in post_models:
            post["title"] = post_model.title
            post["description"] = post_model.description
            post["like_count"] = post_model.like_count
            post["comment_count"] = post_model.comment_count
            post["favorite_count"] = post_model.favorite_count
            post["camp_id"] = post_model.camp_id
            post["category_id"] = post_model.category_id
            post["post_id"] = post_model.id
            posts.append(post)
            post = {}

        if len(posts) == 0:
            posts = None

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        return render_template("lists.html", status="myposts", posts=posts, user=g.user, camp_builders=camp_builders, camp_joins=camp_joins)


class EmailInform(Resource):
    """
    email inform

    """

    method_decorators = [login_required]

    def post(self):
        # get the email inform
        email_inform = request.form.get("switch")
        if email_inform == "True":
            email_inform = True
        else:
            email_inform = False
        # update the email inform in the database
        user = UserModel.query.filter_by(id=g.user.id).first()
        user.email_inform = email_inform
        # database rollback
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.info("{}[{}] failed to update email inform, because the database error.".format(session.get("user_name"), get_user_ip()))
            db.session.rollback()
            raise e
        current_app.logger.info("{}[{}] updated email inform.".format(session.get("user_name"), get_user_ip()))
        return jsonify({"code": 200, "message": "You have changed your email inform successfully! "})


api.add_resource(GetCaptcha, "/captcha")
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Profile, "/profile")
api.add_resource(EditName, "/edit_name")
api.add_resource(EditDescription, "/edit_description")
api.add_resource(EditProfile, "/editprofile")
api.add_resource(UploadAvatar, "/upload_avatar")
api.add_resource(Privacy, "/privacy")
api.add_resource(GetChangePasswordCaptcha, "/get_change_password_captcha")
api.add_resource(EditPassword, "/edit_password")
api.add_resource(DeleteAccount, "/delete_account")
api.add_resource(Logout, "/logout")
api.add_resource(FavoriteContent, "/favorite")
api.add_resource(LikeContent, "/like")
api.add_resource(MyPost, "/myposts")
api.add_resource(EmailInform, "/switch_email")
