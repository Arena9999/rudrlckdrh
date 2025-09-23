from flask import Flask, flash, redirect, render_template, Blueprint, session, request, jsonify, url_for, Response
import sqlite3, cv2

from db import add_user, verify_user, get_user_by_username, get_connection, init_db
from router.users.login import login_bp
from router.users.signup import signup_bp
from router.records.save_photo import save_photo_bp, images_bp
from router.records.video import videos_bp
from router.records.stream import stream_bp
from router.records.videos.full import full_videos_bp
from router.records.videos.highlight import highlight_bp
from router.footerlinks.footer import footer_bp
from templates.user_survice.checklist import checklist_bp

app = Flask(__name__)
app.secret_key = "your secret_key"
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(save_photo_bp)
app.register_blueprint(videos_bp)
app.register_blueprint(stream_bp)
app.register_blueprint(images_bp)
app.register_blueprint(full_videos_bp)
app.register_blueprint(highlight_bp)
app.register_blueprint(footer_bp)
app.register_blueprint(checklist_bp)

init_db()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route("/cva")
def cva():
    return render_template("cva.html")

@app.route("/MT")
def MT():
    return render_template("user_survice/MT.html")

@app.route("/CL")
def CL():
    return render_template("user_survice/cheklist/CL.html")

if __name__ == "__main__":
    app.run(debug=True)