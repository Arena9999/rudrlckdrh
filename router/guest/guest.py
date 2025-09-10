from flask import Blueprint, session, redirect, flash, url_for, render_template

guest_bp = Blueprint("guest", __name__)

@guest_bp.route("/guest")
def guest_home():
    if session.get("user_id") != "guest":
        # 게스트가 아니면 메인 페이지로
        return redirect("/")
    return render_template("guest/guest.html")
