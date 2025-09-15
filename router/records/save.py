from flask import Blueprint, request, jsonify, session
import os, base64, time
from db import get_connection

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

save_bp = Blueprint("save", __name__)

@save_bp.route("/save", methods=["POST"])
def save():
    if "user_id" not in session:
        return jsonify({"error": "로그인 필요"}), 403

    data = request.json
    user_id = session["user_id"]
    cva = data["cva"]
    status = data["status"]
    image_base64 = data["image"]

    if cva is None or status is None or image_base64 is None:
        return jsonify({"error": "값이 올바르지 않습니다"}), 400

    image_bytes = base64.b64decode(image_base64.split(",")[1])
    filename = f"{int(time.time())}_{user_id}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)


    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO cva_records (user_id, cva_value, status, image_path) VALUES (?, ?, ?, ?)",
                (user_id, cva, status, filepath)
            )
            conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "저장 완료"})
