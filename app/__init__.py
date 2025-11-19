from flask import Flask

def start_app():
    app = Flask(__name__)

    from app.controllers.users_controller import users_bp
    from app.controllers.sellers_controller import sellers_bp
    from app.controllers.products_controller import products_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(sellers_bp, url_prefix="/sellers")
    app.register_blueprint(products_bp, url_prefix="/products")

    return app