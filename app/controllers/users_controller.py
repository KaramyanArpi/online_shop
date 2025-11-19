from flask import Blueprint, request, jsonify
from app.services.users_service import UserService
from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)


class UserController:
    def __init__(self):
        pass


    def register_user(self):
        data = request.get_json()
        username, age = data.get("username"), data.get("age")

        try:
            new_user = UserService.register(username, age)
            return jsonify({"user": new_user}), 201
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. Please try again later. {e}"}, 500

    def update_username(self, user_id):
        new_username = request.get_json().get("new_username")

        try:
            updated_user = UserService.update_username(user_id, new_username)
            return jsonify({"updated_user": updated_user})
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. Please try again later. {e}"}, 500

    def delete_user(self, user_id):
        try:
            deleted_user = UserService.delete_user(user_id)
            return jsonify({"deleted_user": deleted_user})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. Please try again later. {e}"}, 500

    def get_user_by_id(self, user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            return jsonify({"user": user})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. {e}"}, 500

    def get_users(self):
        limit = request.args.get("_limit")
        page = request.args.get("page")
        try:
            users = UserService.get_users(limit, page)
            return jsonify({"users": users})
        except InvalidInputError as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. {e}"}, 500


users_bp = Blueprint("users", __name__)
us_controller = UserController()

users_bp.add_url_rule("/register", view_func=us_controller.register_user, methods=["POST"])
users_bp.add_url_rule("/<int:user_id>/update-username", view_func=us_controller.update_username, methods=["PUT"])
users_bp.add_url_rule("/<int:user_id>/delete", view_func=us_controller.delete_user, methods=["DELETE"])
users_bp.add_url_rule("/<int:user_id>", view_func=us_controller.get_user_by_id, methods=["GET"])
users_bp.add_url_rule("/", view_func=us_controller.get_users, methods=["GET"])
