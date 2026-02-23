from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from extensions import db
from models import MusicRequest, DiscordChannel

admin_bp = Blueprint("admin", __name__)

def require_admin():
    if current_user.role != "admin":
        abort(403)

@admin_bp.get("/pending")
@login_required
def pending_view():
    require_admin()
    pending= MusicRequest.query.filter_by(status="PENDING").order_by(MusicRequest.created_at.asc()).all()
    return render_template("admin_dashboard_pending.html", requests=pending)

@admin_bp.get("/all")
@login_required
def all_view():
    require_admin()
    status = request.args.get("status") #optional: APPROVED/DECLINED/PENDING
    q = MusicRequest.query
    if status in {"PENDING", "APPROVED", "DECLINED"}:
        q = q.filter_by(status=status)
    all_reqs = q.order_by(MusicRequest.created_at.desc()).all()
    return render_template("admin_dashboard.html", requests=all_reqs, status=status)

@admin_bp.post("/set-status/<int:req_id>")
@login_required
def set_status(req_id):
    require_admin()
    new_status = request.form["status"] #APPROVED or DECLINED
    if new_status not in {"APPROVED", "DECLINED"}:
        abort(400)
    
    mr = MusicRequest.query.get_or_404(req_id)
    mr.status = new_status
    db.session.commit()

    #user "update" happens automatically because dashboard reads from DB.
    return redirect(request.referrer or url_for("admin.pending_view"))

@admin_bp.get("/channels")
@login_required
def channels_view():
    require_admin()
    channels = DiscordChannel.query.order_by(DiscordChannel.name.asc()).all()
    return render_template("admin_channels.html", channels=channels)

@admin_bp.post("/channels/add")
@login_required
def channels_add():
    require_admin()
    name = request.form.get("name", "").strip()

    if not name:
        return redirect(url_for("admin.channels_view"))
    
    #Prevent duplicates
    exists = DiscordChannel.query.filter_by(name=name).first()
    if not exists:
        db.session.add(DiscordChannel(name=name))
        db.session.commit()
    return redirect(url_for("admin.channels_view"))

@admin_bp.post("/channels/delete/<int:channel_id>")
@login_required
def channels_delete(channel_id):
    require_admin()
    ch = DiscordChannel.query.get_or_404(channel_id)

    #Dont allow deleting channels that are in use.
    in_use = MusicRequest.query.filter_by(channel_id=ch.id).first()
    if in_use:
        flash("Channel in use. Cannot delete.")
        redirect(url_for("admin.channels_view"))
    db.session.delete(ch)
    db.session.commit()
    return redirect(url_for("admin.channels_view"))