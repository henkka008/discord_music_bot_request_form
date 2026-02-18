#first step

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev_change_me"
    app.config["SQLALCHEMY_DATABSE_URI"] = "sqlite:///app.db"
    app.config["SQALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.index"

    from models import User

    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from auth import auth_bp
    from user_routes import user_bp
    from admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
    