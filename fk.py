from flask import Flask, flash, redirect, render_template, Blueprint, session, request, jsonify, url_for, Response
import sqlite3, cv2

from db import database

app = Flask(__name__)
cap = cv2.VideoCapture(0)
app.secret_key = "your secret_key"

database.init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", strict_slashes=False)
def home():
    if "user_id" in session:
        return f"안녕하세요, {session['user_id']}님! <a href='/logout'>로그아웃</a> <a href='/com'>캠</a> <a href='//video_feed'>com</a>"
    return "hello world <br><a href='/login'>로그인</a> <br><a href='/register'>회원가입</a>"


@app.route("/login", methods=["GET", "POST"])
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
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
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

@app.route("/com")
def com():

    return render_template("com.html")



def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame'), "<h1>웹캠 스트리밍</h1><img src='/video_feed'>"




if __name__ == "__main__":
    app.run(debug=True)
