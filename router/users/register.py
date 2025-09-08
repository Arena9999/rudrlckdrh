from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from db import database

register_bp = Blueprint('register', __name__,)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database.add_user(username, password):
            flash("회원가입 완료! 로그인 해주세요.")
            return redirect(url_for("login"))
        else:
            flash("이미 존재하는 사용자입니다.")
            return redirect(url_for("register"))
    return render_template("register.html")
