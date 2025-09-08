from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from db.domains.users.account import database

signup_bp = Blueprint('signup', __name__,)

@signup_bp.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        if not username or not password:
            flash("아이디와 비밀번호를 입력해주세요.")
            return redirect(url_for("signup.register"))

        if password != password_confirm:
            flash("비밀번호가 일치하지 않습니다.")
            return redirect(url_for("signup.register"))

        if database.add_user(username, password):
            flash("회원가입 완료! 로그인 해주세요.")
            return redirect(url_for("login.login"))
        else:
            flash("이미 존재하는 사용자입니다.")
            return redirect(url_for("signup.register"))
    return render_template("signup/signup.html")
