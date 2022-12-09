from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from models import CampModel, CampUserModel
from flask_restful import Resource, Api
import json
from .form import BuildCampForm
from extensions import db, mail


# the information of the blueprint
bp = Blueprint("index", __name__, url_prefix="/")
api = Api(bp)


@api.representation('text/html')
def output_html(data, code, headers=None):
    if isinstance(data, str):
        resp = Response(data)
        return resp
    else:
        return Response(json.dumps(data), mimetype='application/json')


class Index(Resource):
    def get(self):
        return render_template("index.html")


class BuildCamp(Resource):
    def post(self):
        camp_name = request.form.get("camp_name")
        description = request.form.get("description")
        # use form to validate
        form = BuildCampForm(request.form)
        if form.validate():
            # create camp
            camp = CampModel(name=camp_name, description=description)
            # add camp to database
            db.session.add(camp)
            # try and rollback
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            # create camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=g.user.id, identity="Builder")
            # add camp_user to database
            db.session.add(camp_user)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            # redirect to camp page
            return redirect("/")
        else:
            # redirect to camp page
            return redirect("/")


api.add_resource(Index, "/")
api.add_resource(BuildCamp, "/buildcamp")
