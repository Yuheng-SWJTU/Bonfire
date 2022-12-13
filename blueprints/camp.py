import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify, Response
from flask_restful import Resource, Api
import json

from werkzeug.utils import secure_filename

from config import BACKGROUND_UPLOAD_FOLDER, POST_UPLOAD_FOLDER

from models import CampModel, CampUserModel, CategoryModel, UserModel, PostModel, FavoritePostModel, LikePostModel, \
    CommentModel
from extensions import db
from .form import AddCategoryForm
from controller import get_all_camp_builder, get_all_camp_join, get_all_posts, save_all_notice_in_dict, \
    save_all_posts_in_dict, send_comment_notification

from decoration import login_required, check_category

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
    method_decorators = [login_required, check_category]

    def get(self, camp_id):

        # set a session to record the camp_id
        session["camp_id"] = camp_id

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html"), 404
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

        # from session get the sort
        sort = session.get("sort")

        posts = get_all_posts(PostModel, camp_id, sort, None)

        # using post_id to get the username and user_avatar
        for post in posts:
            user = UserModel.query.filter_by(id=post.user_id).first()
            post.username = user.username
            post.user_avatar = user.avatar

        notices_list = save_all_notice_in_dict(PostModel, camp_id)
        posts_list = save_all_posts_in_dict(posts)

        return render_template("camp.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, notices=notices_list,
                               posts=posts_list, page_status="ALL", sort=sort)


class AddCategory(Resource):
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required, check_category]

    def get(self, camp_id):
        session["camp_id"] = camp_id
        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html")
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
                               admins=admin_info, page_status="manage")


class AddAdmin(Resource):
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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
    method_decorators = [login_required]

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


class Posts(Resource):
    method_decorators = [login_required, check_category]

    def get(self, camp_id):

        # set a session to record the camp_id
        session["camp_id"] = camp_id

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html")
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
        return render_template("post.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, page_status="posts")


class MakePost(Resource):
    method_decorators = [login_required]

    def post(self):

        # get the user identity
        user_id = session.get("user_id")

        # get the form data
        post_title = request.form.get("title")
        post_content = request.form.get("content")
        category_id = request.form.get("category_id")
        description = request.form.get("description")
        is_notice = request.form.get("is_notice")
        is_top = request.form.get("is_top")

        if is_notice == "true":
            is_notice = True
        else:
            is_notice = False
        if is_top == "true":
            is_top = True
        else:
            is_top = False

        # check if the post title is empty
        if not post_title:
            return jsonify({"code": 400, "message": "The post title can't be empty!"})
        # check if the post content is empty
        if not post_content:
            return jsonify({"code": 400, "message": "The post content can't be empty!"})
        # check the length of the post title
        if len(post_title) > 50:
            return jsonify({"code": 400, "message": "The length of the post title is too long!"})
        if len(post_title) < 3:
            return jsonify({"code": 400, "message": "The length of the post title is too short!"})
        # check if the category is existed
        if not CategoryModel.query.filter_by(id=category_id).first():
            return jsonify({"code": 400, "message": "The category is not exist!"})

        # if the length of the description is over 150, cut it
        if len(description) > 150:
            description = description[:150]

        # save the post in the database
        post = PostModel()
        post.title = post_title
        post.content = post_content
        post.category_id = category_id
        post.description = description
        post.is_top = is_top
        post.is_notice = is_notice
        post.user_id = user_id
        post.camp_id = session.get("camp_id")
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"code": 400, "message": "Make post failed!"})

        return jsonify({"code": 200})


class ShowPost(Resource):
    method_decorators = [login_required, check_category]

    def get(self, camp_id, category_id, post_id):

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html")
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

        # get the post information
        post = PostModel.query.filter_by(id=post_id, is_delete=0).first()
        if not post:
            return render_template("404.html")

        # format the post update time into "2020-01-01 00:00:00"
        post_update_time = post.update_time.strftime("%Y-%m-%d %H:%M")

        # save the post information in a dictionary
        post_dict = {"post_id": post.id, "post_title": post.title, "post_content": post.content,
                     "post_update_time": post_update_time, "post_username": post.user.username,
                     "post_category_name": post.category.name, "post_camp_id": post.camp_id,
                     "post_category_id": post.category_id, "post_user_id": post.user_id,
                     "post_user_description": post.user.description, "post_user_avatar": post.user.avatar,
                     "post_like_count": post.like_count, "post_comment_count": post.comment_count}

        page_status = category_id

        # get the information of favorite
        favorite = FavoritePostModel.query.filter_by(user_id=user_id, post_id=post_id).first()
        # get the information of like
        like = LikePostModel.query.filter_by(user_id=user_id, post_id=post_id).first()
        # get the information of comment
        comments = CommentModel.query.filter_by(post_id=post_id, is_delete=0).all()
        # store comments in a dictionary
        comments_list = []
        comments_dict = {}
        if comments:
            for comment in comments:
                # format the comment update time into "2020-01-01 00 : 00 : 00"
                comment_create_time = comment.create_time.strftime("%Y-%m-%d %H:%M")
                comments_dict["comment_id"] = comment.id
                comments_dict["comment_content"] = comment.content
                comments_dict["comment_create_time"] = comment_create_time
                comments_dict["comment_username"] = comment.user.username
                comments_dict["comment_user_id"] = comment.user_id
                comments_dict["comment_user_avatar"] = comment.user.avatar
                comments_list.append(comments_dict)
                comments_dict = {}
        else:
            comments_list = None

        if favorite:
            favorite_status = "true"
        else:
            favorite_status = "false"

        if like:
            like_status = "true"
        else:
            like_status = "false"

        return render_template("show.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, post_info=post_dict,
                               page_status=page_status, user_id=user_id, favorite_status=favorite_status,
                               like_status=like_status, comments=comments_list)

    def post(self, camp_id, category_id, post_id):
        # get the post id
        post_id = request.form.get("post_id")
        post = PostModel.query.filter_by(id=post_id).first()
        return jsonify({"code": 200, "post_content": post.content})


class GoToCategory(Resource):
    method_decorators = [login_required, check_category]

    def get(self, camp_id, category_id):
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

        # get the sort in the session
        sort = session.get("sort")

        posts = get_all_posts(PostModel, camp_id, sort, category_id)

        # using post_id to get the username and user_avatar
        for post in posts:
            user = UserModel.query.filter_by(id=post.user_id).first()
            post.username = user.username
            post.user_avatar = user.avatar

        notices_list = save_all_notice_in_dict(PostModel, camp_id)
        posts_list = save_all_posts_in_dict(posts)

        page_status = category_id

        return render_template("camp.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, notices=notices_list,
                               posts=posts_list, page_status=page_status, sort=sort, user_id=user_id)


class Favorite(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the post id
        post_id = request.form.get("post_id")
        # get the post
        post = PostModel.query.filter_by(id=post_id).first()

        # check if the user has already favorite this post
        favorite = FavoritePostModel.query.filter_by(user_id=user_id, post_id=post_id).first()
        if favorite:
            # if the user has already favorite this post, then delete the favorite record
            db.session.delete(favorite)
            db.session.commit()
            # update the post's favorite number
            post.favorite_count -= 1
            db.session.add(post)
            db.session.commit()
            # return the favorite number
            return jsonify({"code": 200, "message": "Cancel favorite", "status": "cancel"})

        # save the favorite post information in the database
        favorite = FavoritePostModel()
        favorite.user_id = user_id
        favorite.post_id = post_id
        db.session.add(favorite)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        # update the post's favorite number
        post.favorite_count += 1
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        return jsonify({"code": 200, "message": "Favorite success.", "status": "success"})


class Like(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the post id
        post_id = request.form.get("post_id")
        # get the post
        post = PostModel.query.filter_by(id=post_id).first()

        # check if the user has already like this post
        like = LikePostModel.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            # if the user has already like this post, then delete the like record
            db.session.delete(like)
            db.session.commit()
            # update the post's like number
            post.like_count -= 1
            db.session.add(post)
            db.session.commit()
            # return the like number
            return jsonify({"code": 200, "message": "Cancel like", "status": "cancel",
                            "like_count": post.like_count})

        # save the like post information in the database
        like = LikePostModel()
        like.user_id = user_id
        like.post_id = post_id
        db.session.add(like)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        # update the post's like number
        post.like_count += 1
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        return jsonify({"code": 200, "message": "Like success.", "status": "success",
                        "like_count": post.like_count})


class DeletePost(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the post id
        post_id = request.form.get("post_id")
        # get the post
        post = PostModel.query.filter_by(id=post_id).first()

        # change the post 'is_delete' to 1
        post.is_delete = 1
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        return jsonify({"code": 200, "message": "Delete success."})


class Comment(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the post id
        post_id = request.form.get("post_id")
        # get the comment content
        content = request.form.get("content")
        if not content:
            return jsonify({"code": 400, "message": "Comment content cannot be empty."})
        if len(content) > 500:
            return jsonify({"code": 400, "message": "Comment content cannot be more than 500 characters."})

        # the comment_count of the post + 1
        post = PostModel.query.filter_by(id=post_id).first()

        # who is the post's author
        post_author = UserModel.query.filter_by(id=post.user_id).first()
        if post_author:
            # if the post's author is not the current user and author opened the comment notification
            if post_author.id != user_id and post_author.email_inform:
                # send the comment notification to the post's author
                send_comment_notification(post_author, post, content)

        post.comment_count += 1
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        # get the comment
        comment = CommentModel()
        comment.user_id = user_id
        comment.post_id = post_id
        comment.content = content
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        return jsonify({"code": 200, "message": "Comment success."})


class DeleteComment(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the comment id
        comment_id = request.form.get("comment_id")
        # get the comment
        comment = CommentModel.query.filter_by(id=comment_id).first()

        # the comment_count of the post - 1
        post = PostModel.query.filter_by(id=comment.post_id).first()
        post.comment_count -= 1
        db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        # change the comment 'is_delete' to 1
        comment.is_delete = 1
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 500, "message": "Server error."})

        return jsonify({"code": 200, "message": "Delete success."})


class UploadImage(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user id
        user_id = session.get("user_id")
        # get the image from wangEditor
        image = request.files.get("wangeditor-uploaded-image")
        if not image:
            return jsonify({"errno": 400, "message": "Image cannot be empty."})

        # check the size of the image
        if image.mimetype not in ["image/jpeg", "image/png", "image/gif", "image/jpg"]:
            return jsonify({"errno": 400, "message": "Image format error."})
        if image.content_length > 1024 * 1024 * 2:
            return jsonify({"errno": 400, "message": "Image size cannot be more than 2M."})
        # check the image format
        # # save the image
        random_name = str(uuid.uuid4())
        image_name = random_name + "." + image.filename.split(".")[-1]
        image.save(os.path.join(POST_UPLOAD_FOLDER, image_name))

        return jsonify({"errno": 0, "data": {
            "url": "/static/upload/posts_images/" + image_name,
            "alt": image_name
        }})


class EditPost(Resource):
    method_decorators = [login_required, check_category]

    def get(self, camp_id, post_id):

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html")
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

        # judge the post is existed
        post = PostModel.query.filter_by(id=post_id, is_delete=0).first()
        if not post:
            return render_template("404.html")
        # judge the user is the author of the post
        if post.user_id == user_id or identity == "Admin" or identity == "Builder":

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
            return render_template("edit.html", camp=camp_dict, categories=categories_list, identity=identity,
                                   camp_builders=camp_builders, camp_joins=camp_joins, page_status="eidt", post=post)
        else:
            return render_template("404.html")


class EditPosts(Resource):
    method_decorators = [login_required]

    def post(self):
        # get the user identity
        user_id = session.get("user_id")

        # get the form data
        post_title = request.form.get("title")
        post_content = request.form.get("content")
        category_id = request.form.get("category_id")
        description = request.form.get("description")
        is_notice = request.form.get("is_notice")
        is_top = request.form.get("is_top")
        post_id = request.form.get("post_id")

        if is_notice == "true":
            is_notice = True
        else:
            is_notice = False
        if is_top == "true":
            is_top = True
        else:
            is_top = False

        # check if the post title is empty
        if not post_title:
            return jsonify({"code": 400, "message": "The post title can't be empty!"})
        # check if the post content is empty
        if not post_content:
            return jsonify({"code": 400, "message": "The post content can't be empty!"})
        # check the length of the post title
        if len(post_title) > 50:
            return jsonify({"code": 400, "message": "The length of the post title is too long!"})
        if len(post_title) < 3:
            return jsonify({"code": 400, "message": "The length of the post title is too short!"})
        # check if the category is existed
        if not CategoryModel.query.filter_by(id=category_id).first():
            return jsonify({"code": 400, "message": "The category is not exist!"})

        # if the length of the description is over 150, cut it
        if len(description) > 150:
            description = description[:150]

        # change the post information
        post = PostModel.query.filter_by(id=post_id).first()
        post.title = post_title
        post.content = post_content
        post.category_id = category_id
        post.description = description
        post.is_notice = is_notice
        post.is_top = is_top
        post.update_time = datetime.now()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"code": 400, "message": "Make post failed!"})

        return jsonify({"code": 200})


class ChangeSort(Resource):
    method_decorators = [login_required]

    def post(self):

        sort = request.form.get("sort")
        if sort == "popularity":
            session["sort"] = "popularity"
        elif sort == "postdate":
            session["sort"] = "postdate"

        return jsonify({"code": 200})


class SearchPost(Resource):
    method_decorators = [login_required, check_category]

    def get(self):
        # get camp_id from session
        camp_id = session.get("camp_id")

        # get the camp information
        camp = CampModel.query.filter_by(id=camp_id).first()
        if camp is None:
            return render_template("404.html"), 404
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

        # from session get the sort
        sort = session.get("sort")

        # get the search content
        search_content = request.args.get("post_search")

        posts = get_all_posts(PostModel, camp_id, sort, None, search_content)

        # using post_id to get the username and user_avatar
        for post in posts:
            user = UserModel.query.filter_by(id=post.user_id).first()
            post.username = user.username
            post.user_avatar = user.avatar

        notices_list = save_all_notice_in_dict(PostModel, camp_id)
        posts_list = save_all_posts_in_dict(posts)

        return render_template("camp.html", camp=camp_dict, categories=categories_list, identity=identity,
                               camp_builders=camp_builders, camp_joins=camp_joins, notices=notices_list,
                               posts=posts_list, page_status="search", sort=sort)


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
api.add_resource(Posts, "/<int:camp_id>/post")
api.add_resource(MakePost, "/make_post")
api.add_resource(ShowPost, "/<int:camp_id>/<int:category_id>/<int:post_id>")
api.add_resource(GoToCategory, "/<int:camp_id>/<int:category_id>")
api.add_resource(Favorite, "/favorite")
api.add_resource(Like, "/like")
api.add_resource(DeletePost, "/delete_post")
api.add_resource(Comment, "/comment")
api.add_resource(DeleteComment, "/delete_comment")
api.add_resource(UploadImage, "/upload_image")
api.add_resource(EditPost, "/<int:camp_id>/<int:post_id>/edit")
api.add_resource(EditPosts, "/edit_post")
api.add_resource(ChangeSort, "/change_sort")
api.add_resource(SearchPost, "/searchpost")
