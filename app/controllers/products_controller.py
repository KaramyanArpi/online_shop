from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)
class ProductController:
    def __init__(self):
        pass

    def register_product(self):
        data = request.get_json()
        title, price, sellers = data.get("title"), data.get("price"), data.get("sellers")

        print(sellers)
        try:
            new_product = ProductService.register(title, price, sellers)
            return jsonify({"product": new_product}), 201
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def update_product(self, product_id):
        new_title = request.get_json().get("new_title")

        try:
            updated_product = ProductService.update_product_title(product_id, new_title)
            return jsonify({"updated_product": updated_product}), 201
        except (NotFoundError, AlreadyExistsError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. Please try again later. {e}"}), 500

    def delete_product(self, seller_id, product_id):
        try:
            result = ProductService.delete_sellers_product(seller_id, product_id)
            return jsonify(result)
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. {e}"}), 500

    def get_sellers_products(self, seller_id):
        page = request.args.get("page")
        limit = request.args.get("_limit")

        try:
            result = ProductService.get_sellers_products(seller_id, page, limit)
            return jsonify(result)
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. {e}"}), 500

    def get_product_by_id(self, product_id):
        try:
            product = ProductService.get_product_by_id(product_id)
            return jsonify({"product": product})
        except (NotFoundError, InvalidInputError) as e:
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            return jsonify({"error": f"Something went wrong. {e}"}), 500


products_bp = Blueprint("products", __name__)
pr_controller = ProductController()

products_bp.add_url_rule("/register", view_func=pr_controller.register_product, methods=["POST"])
products_bp.add_url_rule("/<int:product_id>/update", view_func=pr_controller.update_product, methods=["PUT"])
products_bp.add_url_rule("/<int:seller_id>/<int:product_id>/delete", view_func=pr_controller.delete_product, methods=["DELETE"])
products_bp.add_url_rule("/<int:seller_id>", view_func=pr_controller.get_sellers_products, methods=["GET"])
products_bp.add_url_rule("/<product_id>", view_func=pr_controller.get_product_by_id, methods=["GET"])


