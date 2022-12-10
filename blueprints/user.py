import json
import os
import random
import string
from datetime import datetime
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from controller import handle_error_string, get_all_camp_builder, get_all_camp_join

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from models import UserModel, EmailCaptchaModel, ChangePasswordCaptchaModel
from extensions import db, mail
from .form import RegisterForm, LoginForm, ChangePassword
from werkzeug.security import generate_password_hash, check_password_hash

from config import AVATAR_UPLOAD_FOLDER

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
    def get(self):
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
                # remember me
                rememberme = request.form.getlist("remember")
                if "rememberme" in rememberme:
                    session['remember'] = "true"
                else:
                    session['remember'] = "false"
                print("text")
                return redirect("/")
            else:
                return render_template("login.html", error="Email or password error!")
        else:
            flash("The format of email or password is wrong! ")
            return redirect(url_for("user.login"))


class Register(Resource):
    def get(self):
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
                return redirect(url_for("user.register"))
            return redirect(url_for("user.login"))
        else:
            # get the error message form and handle it from json to string
            flash(handle_error_string(form.errors))
            # flash(form.errors)
            return redirect(url_for("user.register"))


class GetCaptcha(Resource):
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
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "Please deliver your e-mail first! "})


class Profile(Resource):
    def get(self):
        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()
        try:
            return render_template("profile.html", user=g.user, birthday=g.user.birthday.strftime("%Y-%m-%d"),
                               status="profile", camp_builders=camp_builders, camp_joins=camp_joins)
        except Exception as e:
            print(e)
            return render_template("profile.html", user=g.user,
                               status="profile", camp_builders=camp_builders, camp_joins=camp_joins)


class EditName(Resource):
    def post(self):
        new_name = request.form.get("new_name")
        if new_name:
            # check the validation of the name
            if len(new_name) > 20:
                return jsonify({"code": 400, "message": "The length of the name is too long! "})
            if len(new_name) < 4:
                return jsonify({"code": 400, "message": "The length of the name is too short! "})

            # check the name is unique
            user = UserModel.query.filter_by(username=new_name).first()
            if user:
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
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "Please deliver your new name first! "})


class EditDescription(Resource):
    def post(self):
        new_description = request.form.get("new_description")
        if new_description:
            # check the validation of the description
            if len(new_description) > 200:
                return jsonify({"code": 400, "message": "The length of the description is too long! "})

            if len(new_description) < 4:
                return jsonify({"code": 400, "message": "The length of the description is too short! "})

            # update the description in the database
            user_id = session.get("user_id")
            user = UserModel.query.filter_by(id=user_id).first()
            user.description = new_description
            # database rollback
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "Please deliver your new description first! "})


class EditProfile(Resource):
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
            db.session.rollback()
            raise e
        return redirect(url_for("user.profile"))


class UploadAvatar(Resource):
    def post(self):
        # get the file from layui upload component
        file = request.files.get("file")
        if file:
            # check the file format
            if file.filename.split(".")[-1] not in ["jpg", "png", "jpeg"]:
                return jsonify({"code": 400, "message": "The format of the file is wrong! "})
            # check the file size
            if file.content_length > 1024 * 1024 * 2:
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
                db.session.rollback()
                raise e
            return jsonify({"code": 0})
        else:
            return jsonify({"code": 400, "message": "Please deliver your avatar first! "})


class Privacy(Resource):
    def get(self):
        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()
        return render_template("privacy.html", user=g.user,
                                status="privacy", camp_builders=camp_builders, camp_joins=camp_joins)


class GetChangePasswordCaptcha(Resource):
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
                    db.session.rollback()
                    raise e
            else:
                captcha_model = ChangePasswordCaptchaModel(email=email, captcha=captcha, user_id=g.user.id, creat_time=datetime.now())
                db.session.add(captcha_model)
                db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "We cannot detect your email address! "})


class EditPassword(Resource):
    def post(self):
        captcha = request.form.get("captcha")
        password = request.form.get("password")
        password_con = request.form.get("password_con")

        # check the validation of the password
        if len(password) < 6:
            return jsonify({"code": 400, "message": "The length of the password is too short! "})

        if len(password) > 20:
            return jsonify({"code": 400, "message": "The length of the password is too long! "})

        if password != password_con:
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
                    db.session.rollback()
                    raise e
                return jsonify({"code": 200, "message": "You have changed your password successfully! "})
            else:
                return jsonify({"code": 400, "message": "The captcha is wrong! "})


class DeleteAccount(Resource):
    def delete(self):
        # delete the user in the database
        user = UserModel.query.filter_by(id=g.user.id).first()
        # change the username to "Cancelled"
        user.username = "Cancelled"
        # change the email to "Cancelled"
        user.email = "Cancelled"
        # change the password to "Cancelled"
        user.password = "Cancelled"
        # change the avatar to "default.png"
        user.avatar = "default.png"
        # database rollback
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        session.clear()
        return jsonify({"code": 200, "message": "You have deleted your account successfully! "})


class Logout(Resource):
    def get(self):
        # delete the session
        session.clear()
        return redirect(url_for("user.login"))


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


@bp.route("/favorite", methods=["GET", "POST"])
def favorite():
    return render_template("lists.html")
