from flask import Flask, flash, redirect, render_template, Blueprint, session, request, jsonify, url_for, Response
import sqlite3, cv2

from db import add_user, verify_user, get_user_by_username, get_connection, init_db
from router.users.login import login_bp
from router.users.signup import signup_bp
from router.records.save import save_bp
from router.records.records import records_bp

app = Flask(__name__)
app.secret_key = "your secret_key"
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(save_bp)
app.register_blueprint(records_bp)

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

@app.route("/feedback")
def feedback():
    return render_template("footer-links/feedback.html")

@app.route("/FAQ")
def FAQ():
    return render_template("footer-links/FAQ.html")

@app.route("/security")
def security():
    return render_template("footer-links/security.html")

@app.route("/TAC")
def TAC():
    return render_template("footer-links/TAC.html")



if __name__ == "__main__":
    app.run(debug=True)