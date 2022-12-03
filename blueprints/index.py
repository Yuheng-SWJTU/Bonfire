from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_mail import Message


# the information of the blueprint
bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
