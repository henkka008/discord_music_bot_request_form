#first step

from flask import Flask
from extensions import db, login_manager
import os



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev_change_me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ADMIN_INVITE_CODE"] = os.environ.get("ADMIN_INVITE_CODE", "visaisgreat")
    

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.index"

    from models import User

    @login_manager.user_loader
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
    