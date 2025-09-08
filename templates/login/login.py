from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from db.domains.users.account import database

login_bp = Blueprint('/login', __name__,)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if not username or not password:
            flash("아이디와 비밀번호를 입력해주세요.")
            return redirect(url_for("login"))

        user = database.check_user_login(username, password)
        if user:
            session["user_id"] = username
            database.log_login(user["id"], request.remote_addr)
            return redirect(url_for("home"))
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.")
            return redirect(url_for("login"))
    return render_template("login/login.html")
