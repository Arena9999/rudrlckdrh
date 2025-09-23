from flask import Blueprint, request, jsonify, session, render_template
import os
from db import get_connection

videos_bp = Blueprint("records_videos", __name__)  # 이름 고유하게

@videos_bp.route("/videos")
def videos():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM full_videos ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template("videos/videos.html", videos=rows)
