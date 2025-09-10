from flask import Flask, flash, redirect, render_template, Blueprint, session, request, jsonify, url_for, Response
import sqlite3, cv2

from db import database
#from templates.login.login import login_bp
#from templates.signup.signup import signup_bp
from router.users.login import login_bp
from router.users.signup import signup_bp
from router.guest.guest import guest_bp

app = Flask(__name__)
app.secret_key = "your secret_key"
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(guest_bp)

database.init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route("/com")
def com():
    return render_template("com.html")

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