import json
import random
import string
from datetime import datetime
from flask_restful import Resource, Api
from controller import handle_error_string

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from models import UserModel, EmailCaptchaModel
from extensions import db, mail
from .form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

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
                return redirect(url_for("user.login"))
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
            # get the error message form form and handle it from json to string
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
                subject="[Colla] - your register code",
                recipients=[email],
                body=f"Hi, {name} ! \n\n"
                     f"You can enter this code to register into Colla: \n\n"
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


api.add_resource(GetCaptcha, "/captcha")
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")


@bp.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")


@bp.route("/privacy", methods=["GET", "POST"])
def privacy():
    return render_template("privacy.html")


@bp.route("/favorite", methods=["GET", "POST"])
def favorite():
    return render_template("lists.html")
