from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_mail import Message
from flask_restful import Resource, Api
import json
from models import CampModel, CampUserModel, CategoryModel, UserModel
from extensions import db, mail
from .form import AddCategoryForm
from controller import get_all_camp_builder, get_all_camp_join

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

        # set a session to record the camp_id
        session["camp_id"] = camp_id

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        # get the number of people in the camp
        camp_user = CampUserModel.query.filter_by(camp_id=camp_id).all()
        users_num = len(camp_user)
        # Store all camp's information in a dictionary
        camp_dict = {"camp_id": camp.id, "camp_name": camp.name, "camp_description": camp.description,
                     "camp_background": camp.background, "users_num": users_num}

        # get the user identity
        user_id = session.get("user_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"

        # get all category in this camp
        categories = CategoryModel.query.filter_by(camp_id=camp_id).all()
        # store categories in a dictionary
        categories_list = []
        categories_dict = {}
        for category in categories:
            categories_dict["category_id"] = category.id
            categories_dict["category_name"] = category.name
            categories_dict["category_color"] = category.color
            categories_list.append(categories_dict)
            categories_dict = {}

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()
        return render_template("camp.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins)


class AddCategory(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        camp_id = request.form.get("camp_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Admin" or identity == "Builder":
            # get the category name and color
            category_name = request.form.get("category_name")
            category_color = request.form.get("category_color")
            # check whether the category name is exist
            category = CategoryModel.query.filter_by(name=category_name, camp_id=camp_id).first()
            if category:
                return jsonify({"code": 400, "message": "This category has been added!"})
            # using form to check the category name and color
            form = AddCategoryForm(request.form)
            if form.validate():
                # add the category to the database
                category = CategoryModel(name=category_name, color=category_color, camp_id=camp_id)
                db.session.add(category)
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return jsonify({"code": 400, "message": "Add category failed!"})
                return jsonify({"code": 200})
            else:
                return jsonify({"code": 400, "message": "Please check your input!"})
        else:
            return jsonify({"code": 400, "message": "You don't have the permission!"})


class EditCategory(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        # get the camp_id from g
        camp_id = session.get("camp_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Admin" or identity == "Builder":
            # get the category name and color
            category_name = request.form.get("category_name")
            category_color = request.form.get("category_color")
            category_id = request.form.get("category_id")
            # check whether the category name is exist
            category = CategoryModel.query.filter_by(name=category_name, camp_id=camp_id).first()
            if category:
                return redirect("/camp/" + str(camp_id))
            # using form to check the category name and color
            # add the category to the database
            category = CategoryModel.query.filter_by(id=category_id).first()
            category.name = category_name
            category.color = category_color
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return redirect("/camp/" + str(camp_id))
            return redirect("/camp/" + str(camp_id))
        else:
            return redirect("/camp/" + str(camp_id))


class DeleteCategory(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        # get the camp_id from g
        camp_id = session.get("camp_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Admin" or identity == "Builder":
            # get the category id
            category_id = request.form.get("category_id")
            # delete the category
            category = CategoryModel.query.filter_by(id=category_id).first()
            db.session.delete(category)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Delete category failed!"})
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "You don't have the permission!"})


class LeaveCamp(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        # get the camp_id from g
        camp_id = session.get("camp_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Builder":
            return jsonify({"code": 400, "message": "You are the builder of this camp, you can't leave!"})
        else:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            db.session.delete(camp_user)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Leave camp failed!"})
            # clear the camp_id in session
            session["camp_id"] = None
            return jsonify({"code": 200})


class ManageCamp(Resource):
    def get(self, camp_id):
        session["camp_id"] = camp_id
        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        # get the number of people in the camp
        camp_user = CampUserModel.query.filter_by(camp_id=camp_id).all()
        users_num = len(camp_user)
        # Store all camp's information in a dictionary
        camp_dict = {"camp_id": camp.id, "camp_name": camp.name, "camp_description": camp.description,
                     "camp_background": camp.background, "users_num": users_num}

        # get the user identity
        user_id = session.get("user_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"

        # get all category in this camp
        categories = CategoryModel.query.filter_by(camp_id=camp_id).all()
        # store categories in a dictionary
        categories_list = []
        categories_dict = {}
        for category in categories:
            categories_dict["category_id"] = category.id
            categories_dict["category_name"] = category.name
            categories_dict["category_color"] = category.color
            categories_list.append(categories_dict)
            categories_dict = {}

        camp_builders = get_all_camp_builder()
        camp_joins = get_all_camp_join()

        # get the builder information of this camp
        # format: {"user_id": user_id, "user_name": user_name, "user_avatar": user_avatar}
        builder_info = {}
        camp_builder = CampUserModel.query.filter_by(camp_id=camp_id, identity="Builder").first()
        if camp_builder:
            builder = UserModel.query.filter_by(id=camp_builder.user_id).first()
            builder_info["user_id"] = builder.id
            builder_info["user_name"] = builder.username
            builder_info["user_avatar"] = builder.avatar

        # get the admin information of this camp
        # format: {"user_id": user_id, "user_name": user_name, "user_avatar": user_avatar}
        admin_info = []
        camp_admins = CampUserModel.query.filter_by(camp_id=camp_id, identity="Admin").all()
        for camp_admin in camp_admins:
            admin = UserModel.query.filter_by(id=camp_admin.user_id).first()
            admin_dict = {"user_id": admin.id, "user_name": admin.username, "user_avatar": admin.avatar}
            admin_info.append(admin_dict)
        if not admin_info:
            admin_info = None

        return render_template("manage.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, builder=builder_info,
                               admins=admin_info)


class AddAdmin(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        camp_id = request.form.get("camp_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Builder":
            # get the user_id of the new admin
            new_admin_name = request.form.get("username")
            # get the user model of the new admin
            new_admin = UserModel.query.filter_by(username=new_admin_name).first()
            # if the user is not exist
            if not new_admin:
                return jsonify({"code": 400, "message": "The user is not exist!"})
            # get the camp_user model of the new admin
            new_admin_camp_user = CampUserModel.query.filter_by(user_id=new_admin.id, camp_id=camp_id).first()
            # check if the user is not in this camp
            if not new_admin_camp_user:
                return jsonify({"code": 400, "message": "This user is not in this camp!"})
            # check if the new admin is already an admin
            elif new_admin_camp_user.identity == "Admin":
                return jsonify({"code": 400, "message": "This user is already an admin!"})
            # check if the new admin is the builder
            elif new_admin_camp_user.identity == "Builder":
                return jsonify({"code": 400, "message": "You are the builder of this camp!"})
            else:
                new_admin_camp_user.identity = "Admin"
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return jsonify({"code": 400, "message": "Add admin failed!"})
                return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "You don't have the permission!"})


api.add_resource(Camp, "/<int:camp_id>")
api.add_resource(AddCategory, "/add_category")
api.add_resource(EditCategory, "/editcategory")
api.add_resource(DeleteCategory, "/delete_category")
api.add_resource(LeaveCamp, "/leave_camp")
api.add_resource(ManageCamp, "/<int:camp_id>/manage")
api.add_resource(AddAdmin, "/add_admin")


@bp.route("/post", methods=["GET", "POST"])
def post():
    return render_template("post.html")


@bp.route("/show", methods=["GET", "POST"])
def show():
    return render_template("show.html")
