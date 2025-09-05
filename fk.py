from flask import Flask, render_template, Blueprint, session, request, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "your secret_key"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def hello():
    return "hello world"

@app.route("/templates/login")
def login():
    return 0


if __name__ == "__main__":
    app.run()



