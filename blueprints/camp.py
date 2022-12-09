from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from flask_restful import Resource, Api
import json
from models import CampModel, CampUserModel


# the information of the blueprint
bp = Blueprint("camp", __name__, url_prefix="/camp")
api = Api(bp)


@api.representation('text/html')
def output_html(data, code, headers=None):
    if isinstance(data, str):
        resp = Response(data)
        return resp
    else:
        return Response(json.dumps(data), mimetype='application/json')


class Camp(Resource):
    def get(self, camp_id):

        return render_template("camp.html")


api.add_resource(Camp, "/<int:camp_id>")


@bp.route("/post", methods=["GET", "POST"])
def post():
    return render_template("post.html")


@bp.route("/show", methods=["GET", "POST"])
def show():
    return render_template("show.html")


@bp.route("/manage", methods=["GET", "POST"])
def manage():
    return render_template("manage.html")


