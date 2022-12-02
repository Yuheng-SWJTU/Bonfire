from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_mail import Message


# the information of the blueprint
bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
