from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from models import CampModel, CampUserModel
from flask_restful import Resource, Api
import json
from .form import BuildCampForm
from extensions import db, mail
from controller import get_all_camp_builder, get_all_camp_join


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
        # get all camps
        camps = CampModel.query.all()
        # Count the people in each camp
        camp_user = CampUserModel.query.all()
        users_in_camp = {}
        for camp in camps:
            users_in_camp[camp.id] = 0
        for user in camp_user:
            users_in_camp[user.camp_id] += 1
        print(users_in_camp)
        # store camps in a dictionary
        camps_list = []
        camps_dict = {}
        for camp in camps:
            camps_dict["camp_id"] = camp.id
            camps_dict["camp_name"] = camp.name
            camps_dict["camp_description"] = camp.description
            camps_dict["camp_background"] = camp.background
            # get the number of people in the camp
            camps_dict["users_num"] = users_in_camp[camp.id]
            camps_list.append(camps_dict)
            camps_dict = {}
        # print(camps_list)

        # get all camps which identity is "Builder"
        # save the camp_id and camp_name in a dictionary
        # format: {"camp_id": camp_id, "camp_name": camp_name}

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        return render_template("index.html", camps=camps_list, camp_builders=camp_builders, camp_joins=camp_joins)


class BuildCamp(Resource):
    def post(self):
        camp_name = request.form.get("camp_name")
        description = request.form.get("description")
        # if camp_name is exist
        if CampModel.query.filter_by(name=camp_name).first():
            flash("This camp name is already exist.")
            return redirect("/")
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


class JoinCamp(Resource):
    def post(self):
        # handle the request from ajax
        camp_id = request.form.get("camp_id")
        # if user is already in the camp
        if CampUserModel.query.filter_by(camp_id=camp_id, user_id=g.user.id).first():
            return jsonify({"code": 400, "message": "You are already in the camp."})
        # create camp_user
        camp_user = CampUserModel(camp_id=camp_id, user_id=g.user.id, identity="Member")
        # add camp_user to database
        db.session.add(camp_user)
        # try and rollback
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        users_num = CampUserModel.query.filter_by(camp_id=camp_id).count()
        return jsonify({"code": 200, "message": "Join camp successfully.", "users_num": users_num, "camp_id": camp_id})


api.add_resource(Index, "/")
api.add_resource(BuildCamp, "/buildcamp")
api.add_resource(JoinCamp, "/join_camp")
