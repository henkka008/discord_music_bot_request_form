from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/")
def index():
    return render_template("index.html")

@auth_bp.get("/login/user")
def login_user_page():
    return render_template("login_user.html")

@auth_bp.get("/login/admin")
def login_admin_page():
    return render_template("login_admin.html")

@auth_bp.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"] # either "user" or "admin"

    user = User.query.filter_by(username=username, role=role).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash("Invalid credentials")
        return redirect(url_for("auth.index"))
    
    login_user(user)
    if role == "admin":
        return redirect(url_for("admin.pending_view"))
    return redirect(url_for("user.dashboard"))

@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.index"))