from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

#Index
@auth_bp.get("/")
def index():
    return render_template("index.html")

#Login pages
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
    return redirect(url_for("admin.pending_view" if role == "admin" else "user.dashboard"))

#Register user
@auth_bp.get("/register")
def register_page():
    return render_template("register_user.html")

@auth_bp.post("/register")
def register_post():
    username = request.form["username"].strip()
    password = request.form["password"]

    if not username or not password:
        flash("Username and password required")
        return redirect(url_for("auth.register_page"))
    
    #Block duplicate usernames across both roles
    if User.query.filter_by(username=username).first():
        flash("Username already taken")
        return redirect(url_for("auth.register_page"))
    
    new_user = User(
        username=username,
        role="user",
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    flash("Account created! Please log in.")
    return redirect(url_for("auth.login_user_page"))

#Register admin
@auth_bp.get("/register/admin")
def register_admin_page():
    return render_template("register_admin.html")

@auth_bp.post("/register/admin")
def register_admin_post():
    username = request.form["username"].strip()
    password = request.form["password"]
    invite_code = request.form["invite_code"].strip()

    if invite_code != current_app.config["ADMIN_INVITE_CODE"]:
        flash("Invalid admin invite code")
        return redirect(url_for("auth.register_admin_page"))
    
    if not username or not password:
        flash("Username and password required")
        return redirect(url_for("auth.register_admin_page"))
    
    if User.query.filter_by(username=username).first():
        flash("Username already taken")
        return redirect(url_for("auth.register_admin_page"))
    
    admin = User(
        username=username,
        role="admin",
        password_hash=generate_password_hash(password)
    )
    db.session.add(admin)
    db.session.commit()

    flash("Admin account created! Please log in.")
    return redirect(url_for("auth.login_admin_page"))



#Logout
@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.index"))