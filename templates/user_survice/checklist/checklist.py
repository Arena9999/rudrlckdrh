from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection

checklist_bp = Blueprint("checklist", __name__)

# 체크리스트 항목 키
FACTORS = [
    "long_computer_time",
    "low_monitor",
    "slouching",
    "no_breaks",
    "phone_neck",
    "weak_back",
    "eye_headache"
]

@checklist_bp.route("/checklist", methods=["GET", "POST"])
def checklist():
    # 로그인 연동 전이라면 테스트용 user_id
    user_id = session.get("user_id", 1)  

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        # 체크된 항목 리스트
        checked_factors = request.form.getlist("factors")  

        # 각 factor를 DB에 저장 (체크=1, 미체크=0)
        for factor in FACTORS:
            is_checked = 1 if factor in checked_factors else 0
            cur.execute("""
                INSERT INTO checklist (user_id, factor_key, checked)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, factor_key) DO UPDATE SET
                  checked=excluded.checked,
                  updated_at=CURRENT_TIMESTAMP
            """, (user_id, factor, is_checked))

        conn.commit()
        conn.close()
        return redirect(url_for("checklist.checklist"))  # 제출 후 페이지 새로고침

    # GET 요청: 유저 체크리스트 불러오기
    cur.execute("SELECT factor_key, checked FROM checklist WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    saved_data = {row["factor_key"]: row["checked"] for row in rows}
    conn.close()

    return render_template("checklist/CL.html", saved_data=saved_data)
