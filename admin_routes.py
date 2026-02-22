from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from models import MusicRequest

admin_bp = Blueprint("admin", __name__)

def require_admin():
    if current_user.role != "admin":
        abort(403)

@admin_bp.get("/pending")
@login_required
def pending_view():
    require_admin()
    pending= MusicRequest.query.filter_by(status="PENDING").order_by(MusicRequest.created_at.asc()).all()
    return render_template("admin_dashboard_pending_html", request=pending)

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