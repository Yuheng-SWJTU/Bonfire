from flask import Blueprint, render_template, request, redirect, flash, g, session, jsonify, Response, current_app
from models import CampModel, CampUserModel
from flask_restful import Resource, Api
import json
from .form import BuildCampForm
from extensions import db
from controller import get_all_camp_builder, get_all_camp_join, get_user_ip
from decoration import login_required
from sqlalchemy import or_


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

    method_decorators = [login_required]

    def get(self):
        # clear the camp_id session
        session["camp_id"] = None
        # get all camps
        camps = CampModel.query.all()
        # Count the people in each camp
        camp_user = CampUserModel.query.all()
        users_in_camp = {}
        for camp in camps:
            users_in_camp[camp.id] = 0
        for user in camp_user:
            users_in_camp[user.camp_id] += 1
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

        if len(camps_list) == 0:
            camps_list = None

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        return render_template("index.html", camps=camps_list, camp_builders=camp_builders, camp_joins=camp_joins)


class BuildCamp(Resource):

    method_decorators = [login_required]

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
                current_app.logger.error("{}[{}] {}".format(session.get("user_name"), get_user_ip(), e))
                db.session.rollback()
            # create camp_user
            camp_user = CampUserModel(camp_id=camp.id, user_id=g.user.id, identity="Builder")
            # add camp_user to database
            db.session.add(camp_user)
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.error("{}[{}] {}".format(session.get("user_name"), get_user_ip(), e))
                db.session.rollback()
            # redirect to the camp page
            current_app.logger.info("{}[{}] build camp {}".format(session.get("user_name"), get_user_ip(), camp_name))
            return redirect("/camp/" + str(camp.id) + "/manage")
        else:
            # redirect to camp page
            return redirect("/")


class JoinCamp(Resource):

    method_decorators = [login_required]

    def post(self):
        # handle the request from ajax
        camp_id = request.form.get("camp_id")
        # if user is already in the camp
        if CampUserModel.query.filter_by(camp_id=camp_id, user_id=g.user.id).first():
            current_app.logger.info("{}[{}] has already in camp {}".format(session.get("user_name"), get_user_ip(), camp_id))
            return jsonify({"code": 400, "message": "You are already in the camp."})
        # create camp_user
        camp_user = CampUserModel(camp_id=camp_id, user_id=g.user.id, identity="Member")
        # add camp_user to database
        db.session.add(camp_user)
        # try and rollback
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error("{}[{}] {}".format(session.get("user_name"), get_user_ip(), e))
            db.session.rollback()
        users_num = CampUserModel.query.filter_by(camp_id=camp_id).count()
        current_app.logger.info("{}[{}] join a camp: {}".format(session.get("user_name"), get_user_ip(), camp_id))
        return jsonify({"code": 200, "message": "Join camp successfully.", "users_num": users_num, "camp_id": camp_id})


class SearchCamp(Resource):

        method_decorators = [login_required]

        def get(self):
            # get the search content
            search_content = request.args.get("index_search")
            # get all camps
            camps = CampModel.query.filter(or_
                                           (CampModel.name.like("%" + search_content + "%"),
                                            CampModel.description.like("%" + search_content + "%"))
                                           )
            # Count the people in each camp
            camp_user = CampUserModel.query.all()
            users_in_camp = {}
            for camp in camps:
                try:
                    users_in_camp[camp.id] = 0
                except Exception as e:
                    current_app.logger.error("{}[{}] {}".format(session.get("user_name"), get_user_ip(), e))
                    continue
            for user in camp_user:
                try:
                    users_in_camp[user.camp_id] += 1
                except Exception as e:
                    current_app.logger.error("{}[{}] {}".format(session.get("user_name"), get_user_ip(), e))
                    continue
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

            camp_builders = get_all_camp_builder()
            camp_joins = get_all_camp_join()

            if len(camps_list) == 0:
                camps_list = None

            return render_template("index.html", camps=camps_list, camp_builders=camp_builders, camp_joins=camp_joins)


api.add_resource(Index, "/")
api.add_resource(BuildCamp, "/buildcamp")
api.add_resource(JoinCamp, "/join_camp")
api.add_resource(SearchCamp, "/searchcamp")
