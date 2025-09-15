from flask import Blueprint, render_template, redirect, url_for, session
from db import get_connection 

records_bp = Blueprint("records", __name__)

@records_bp.route("/records")
def records():
    if "user_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_connection()
    rows = conn.execute(
        "SELECT cva_value, status, image_path, created_at FROM cva_records WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("records.html", records=rows, username=session.get("username"))
