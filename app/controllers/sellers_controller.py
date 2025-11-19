from flask import Blueprint, request, jsonify
from app.services.sellers_service import SellerService
from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)

class SellerController:
    def __init__(self):
        pass

    def seller_register(self):
        data = request.get_json()
        name, rating = data.get("name"), data.get("rating")

        try:
            new_seller = SellerService.register(name, rating)
            return jsonify({"seller": new_seller})
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def update_seller(self, seller_id):
        new_name = request.get_json().get("new_name")

        try:
            updated_seller = SellerService.update_name(seller_id, new_name)
            return jsonify({"updated_seller": updated_seller}), 201
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def delete_seller(self, seller_id):
        try:
            deleted_seller = SellerService.delete_seller(seller_id)
            return jsonify({"deleted_seller": deleted_seller})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def get_seller_by_id(self, seller_id):
        try:
            seller = SellerService.get_seller_by_id(seller_id)
            return jsonify({"seller": seller})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def get_sellers(self):
        page = request.args.get("page")
        limit = request.args.get("_limit")

        try:
            sellers = SellerService.get_sellers(page, limit)
            return jsonify({"sellers": sellers})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500


sellers_bp = Blueprint("sellers", __name__)
sel_controller = SellerController()

sellers_bp.add_url_rule("/register", view_func=sel_controller.seller_register, methods=["POST"])
sellers_bp.add_url_rule("/<int:seller_id>/update", view_func=sel_controller.update_seller, methods=["PUT"])
sellers_bp.add_url_rule("/<int:seller_id>/delete", view_func=sel_controller.delete_seller, methods=["DELETE"])
sellers_bp.add_url_rule("/<int:seller_id>", view_func=sel_controller.get_seller_by_id, methods=["GET"])
sellers_bp.add_url_rule("/", view_func=sel_controller.get_sellers, methods=["GET"])