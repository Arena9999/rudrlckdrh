from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection
from datetime import datetime, timedelta

checklist_bp = Blueprint("checklist", __name__)

# 체크리스트 영어 key → 한국어 문장 매핑
FACTOR_KR = {
    "Cold, tingling hands and feet, and poor posture.": "손발이 차고 자주 저리고, 평소 구부정한 자세라는 말을 자주 듣는다.",
    "Neck cracking, frequent fatigue, and headaches.": "목을 이리저리 돌렸을 때 우두둑하는 소리가 나거나 쉽게 피곤하고 두통이 자주 생긴다.",
    "Bad sleeping habit.": "잠 버릇이 나쁘다.",
    "Over 8 hours of computer use daily.": "컴퓨터를 하루에 8시간 이상 하는 편이다.",
    "Frequent neck and shoulder stiffness.": "목과 어깨가 자주 결린다.",
    "Unrefreshing sleep.": "자고 일어났을 때 개운하지 않다.",
    "Eye strain and chronic headaches.": "눈이 쉽게 뻐근하고 만성 두통에 시달린다."
}

FACTORS = list(FACTOR_KR.keys())

# DB에 체크리스트 저장 (중복 방지 + UPDATE)
def save_checklist(user_id, factors, all_factors):
    conn = get_connection()
    cur = conn.cursor()
    try:
        kst_now = datetime.utcnow() + timedelta(hours=9)
        for factor in all_factors:
            is_checked = 1 if factor in factors else 0

            # 기존 row 확인
            cur.execute(
                "SELECT id FROM checklist WHERE user_id=? AND factor_key=?",
                (user_id, factor)
            )
            row = cur.fetchone()

            if row:
                # 이미 존재하면 UPDATE
                cur.execute("""
                    UPDATE checklist
                    SET checked=?, updated_at=?
                    WHERE user_id=? AND factor_key=?
                """, (is_checked, kst_now, user_id, factor))
            else:
                # 존재하지 않으면 INSERT
                cur.execute("""
                    INSERT INTO checklist (user_id, factor_key, checked, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (user_id, factor, is_checked, kst_now))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error saving checklist:", e)
    finally:
        conn.close()

# DB에서 유저의 체크리스트 불러오기
def get_user_checklist(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT factor_key, checked FROM checklist WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return {row["factor_key"]: row["checked"] for row in rows}

# 라우트
@checklist_bp.route("/CL", methods=["GET", "POST"])
def checklist():
    # 로그인 연동
    if "user_id" not in session:
        return redirect(url_for("auth.login"))  # 로그인 페이지로 이동

    user_id = session["user_id"]

    if request.method == "POST":
        checked_factors = request.form.getlist("factors")
        # FACTORS 리스트에 있는 값만 필터링 (보안)
        checked_factors = [f for f in checked_factors if f in FACTORS]
        save_checklist(user_id, checked_factors, FACTORS)
        return redirect(url_for("checklist.checklist"))

    saved_data = get_user_checklist(user_id)
    return render_template(
        "user_service/CL.html",
        saved_data=saved_data,
        FACTORS=FACTORS
    )

@checklist_bp.route("/CL/view", methods=["GET"])
def view_checklist():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    saved_data = get_user_checklist(user_id)  # {factor_key: checked}

    # checked된 항목만 필터링 + 한국어 매핑
    checked_items = [
        FACTOR_KR[factor] for factor, checked in saved_data.items() if checked
    ]

    return render_template(
        "user_service/CL_view.html",
        checked_items=checked_items
    )
