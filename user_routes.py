from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from extensions import db
from models import MusicRequest, DiscordChannel

user_bp = Blueprint("user", __name__)

def require_user():
    if current_user.role != "user":
        abort(403)

@user_bp.get("/dashboard")
@login_required
def dashboard():
    require_user()
    requests_q = MusicRequest.query.filter_by(user_id=current_user.id).order_by(MusicRequest.created_at.desc()).all()
    return render_template("user_dashboard.html", requests=requests_q)

@user_bp.get("/new")
@login_required
def new_form():
    require_user()
    channels = DiscordChannel.query.order_by(DiscordChannel.name).all()
    return render_template("request_form.html", channels=channels, mode="create")

@user_bp.post("/new")
@login_required
def create_form():
    require_user()

    #Expecing HTML inputs:
    #date_from, date_to as DD-MM-YYYY
    #time_from, time_to as HH:MM
    date_from = datetime.strptime(request.form["date_from"], "%Y-%m-%d").date()
    date_to = datetime.strptime(request.form["date_to"], "%Y-%m-%d").date()
    time_from = datetime.strptime(request.form["time_from"], "%H:%M").time()
    time_to =datetime.strptime(request.form["time_to"], "%H:%M").time()

    channel_id = int(request.form["channel_id"])
    music_type = request.form["music_type"].strip()

    mr = MusicRequest(
        date_from=date_from,
        date_to=date_to,
        time_from=time_from,
        time_to=time_to,
        channel_id=channel_id,
        music_type=music_type,
        status="PENDING",
        user_id=current_user.id
    )
    db.session.add(mr)
    db.session.commit()

    #"Send to admin" in MVP just means: it exists in DB as PENDING.
    return redirect(url_for("user.dashboard"))

@user_bp.get("/edit/<int:req_id>")
@login_required
def edit_form(req_id):
    require_user()
    mr = MusicRequest.query.get_or_404(req_id)
    if mr.user_id != current_user.id:
        abort(403)
    if mr.status != "PENDING":
        abort(400) #optonal rule: only edit pending
    
    channels = DiscordChannel.query.order_by(DiscordChannel.name).all()
    return render_template("request_form.html", channels=channels, req=mr, mode="edit")

@user_bp.post("/edit/<int:req_id>")
@login_required
def update_form(req_id):
    require_user()
    mr = MusicRequest.query.get_or_404(req_id)
    if mr.user_id != current_user.id:
        abort(403)
    if mr.status != "PENDING":
        abort(400)
    
    mr.date_from = datetime.strptime(request.form["date_from"], "%d-%m-%Y").date()
    mr.date_to = datetime.strptime(request.form["date_to"], "%d-%m-%Y").date()
    mr.time_from = datetime.strptime(request.form["time_from"], "%H:%M").time()
    mr.time_to =datetime.strptime(request.form["time_to"], "%H:%M").time()
    mr.channel_id = int(request.form["channel_id"])
    mr.music_type = request.form["music_type"].strip()
    
    db.session.commit()
    return redirect(url_for("user.dashboard"))

@user_bp.post("/delete/<int:req_id>")
@login_required
def delete_form(req_id):
    require_user()
    mr = MusicRequest.query.get_or_404(req_id)
    if mr.user_id != current_user.id:
        abort(403)
    if mr.status != "PENDING":
        abort(400)
    
    db.session.delete(mr)
    db.session.commit()
    return redirect(url_for("user.dashboard"))