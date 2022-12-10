import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_restful import Resource, Api
import json

from werkzeug.utils import secure_filename

from config import BACKGROUND_UPLOAD_FOLDER

from models import CampModel, CampUserModel, CategoryModel, UserModel
from extensions import db
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


class RemoveAdmin(Resource):
    def post(self):
        # get the user identity
        user_id = session.get("user_id")
        camp_id = request.form.get("camp_id")
        admin_id = request.form.get("admin_id")
        if user_id:
            camp_user = CampUserModel.query.filter_by(user_id=user_id, camp_id=camp_id).first()
            if camp_user:
                identity = camp_user.identity
            else:
                identity = "visitor"
        else:
            identity = "visitor"
        if identity == "Builder":
            # get the user model of the admin
            admin = UserModel.query.filter_by(id=admin_id).first()
            # if the user is not exist
            if not admin:
                return jsonify({"code": 400, "message": "The user is not exist!"})
            # get the camp_user model of the new admin
            delete_admin_camp_user = CampUserModel.query.filter_by(user_id=admin.id, camp_id=camp_id).first()
            # check if the user is not in this camp
            if not delete_admin_camp_user:
                return jsonify({"code": 400, "message": "This user is not in this camp!"})
            # change the identity of the admin
            delete_admin_camp_user.identity = "Member"
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Remove admin failed!"})
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "You don't have the permission!"})


class UploadBackground(Resource):
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

            # before save the file, check if the camp has a background
            camp = CampModel.query.filter_by(id=session.get("camp_id")).first()
            if camp.background != "default_camp.png":
                # delete the old background
                os.remove(os.path.join(BACKGROUND_UPLOAD_FOLDER, camp.background))

            # save the file
            # change the file name into camp_id + file format
            file_name = str(session.get("camp_id")) + "." + file.filename.split(".")[-1]
            file_name = secure_filename(file_name)
            file.save(os.path.join(BACKGROUND_UPLOAD_FOLDER, file_name))
            # save the file name in the database
            camp = CampModel.query.filter_by(id=session.get("camp_id")).first()
            camp.background = file_name
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Upload background failed!"})
            return jsonify({"code": 0})
        else:
            return jsonify({"code": 400, "message": "Please deliver your background image first! "})


class EditCamp(Resource):
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
        if identity == "Builder" or identity == "Admin":
            # get the camp model
            camp = CampModel.query.filter_by(id=camp_id).first()
            # get the form data
            camp_name = request.form.get("camp_name")
            camp_description = request.form.get("camp_description")
            # check if the camp name is empty
            if not camp_name:
                return jsonify({"code": 400, "message": "The camp name can't be empty!"})
            # check if the camp description is empty
            if not camp_description:
                return jsonify({"code": 400, "message": "The camp description can't be empty!"})
            # check the length of the camp name
            if len(camp_name) > 20:
                return jsonify({"code": 400, "message": "The length of the camp name is too long!"})
            if len(camp_name) < 3:
                return jsonify({"code": 400, "message": "The length of the camp name is too short!"})
            # check the length of the camp description
            if len(camp_description) > 100:
                return jsonify({"code": 400, "message": "The length of the camp description is too long!"})
            if len(camp_description) < 3:
                return jsonify({"code": 400, "message": "The length of the camp description is too short!"})
            # check if the camp name is already exist
            if CampModel.query.filter_by(name=camp_name).first() and camp.name != camp_name:
                return jsonify({"code": 400, "message": "The camp name is already exist!"})
            # update the camp model
            camp.name = camp_name
            camp.description = camp_description
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Edit camp failed!"})
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "You don't have the permission!"})


class DismissCamp(Resource):
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

            # delete the camp background image in the folder
            camp = CampModel.query.filter_by(id=camp_id).first()
            if camp.background != "default_camp.png":
                os.remove(os.path.join(BACKGROUND_UPLOAD_FOLDER, camp.background))

            # delete the data in the CampUserModel
            camp_users = CampUserModel.query.filter_by(camp_id=camp_id).all()
            for camp_user in camp_users:
                db.session.delete(camp_user)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Dismiss camp failed!"})

            # delete the data in the CampModel
            camp = CampModel.query.filter_by(id=camp_id).first()
            db.session.delete(camp)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "message": "Dismiss camp failed!"})

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
api.add_resource(RemoveAdmin, "/remove_admin")
api.add_resource(UploadBackground, "/upload_background")
api.add_resource(EditCamp, "/edit_camp")
api.add_resource(DismissCamp, "/dismiss_camp")


@bp.route("/post", methods=["GET", "POST"])
def post():
    return render_template("post.html")


@bp.route("/show", methods=["GET", "POST"])
def show():
    return render_template("show.html")
