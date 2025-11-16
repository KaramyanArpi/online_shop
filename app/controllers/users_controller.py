from flask import Blueprint, request, jsonify
from app.services.users_service import UserService
from app.db import get_db
from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)


class UserController:
    def __init__(self):
        self.db = get_db()
        self.user_service = UserService(self.db)

    def register_user(self):
        data = request.get_json()
        username, age = data.get("username"), data.get("age")

        try:
            new_user = self.user_service.register(username, age)
            return jsonify({"user": new_user}), 201
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. Please try again later. {e}"}, 500

    def update_username(self, user_id):
        new_username = request.get_json().get("new_username")

        try:
            updated_user = self.user_service.update_username(user_id, new_username)
            return jsonify({"updated_user": updated_user})
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return {"error": f"Something went wrong. Please try again later. {e}"}, 500



users_bp = Blueprint("users", __name__)
us_controller = UserController()

users_bp.add_url_rule("/register", view_func=us_controller.register_user, methods=["POST"])
users_bp.add_url_rule("/<int:user_id>/update-username", view_func=us_controller.update_username, methods=["PUT"])
