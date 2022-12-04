from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_mail import Message


# the information of the blueprint
bp = Blueprint("camp", __name__, url_prefix="/camp")


@bp.route("/", methods=["GET", "POST"])
def camp():
    return render_template("camp.html")
