from flask import Flask, flash, redirect, render_template, Blueprint, session, request, jsonify, url_for, Response
import sqlite3, cv2

from db.domains.users.account import database
from templates.login.login import login_bp
from templates.signup.signup import signup_bp

app = Flask(__name__)
app.secret_key = "your secret_key"

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)

database.init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/com")
def com():
    return render_template("com.html")



if __name__ == "__main__":
    app.run(debug=True)