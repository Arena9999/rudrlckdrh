from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection
from datetime import datetime, timedelta

user_service_bp = Blueprint("user_service", __name__)

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

# 영어 key 리스트
FACTORS = list(FACTOR_KR.keys())

# 영어 key → DB column 이름 매핑
FACTOR_COLUMNS = {
    "Cold, tingling hands and feet, and poor posture.": "cold_tingling_posture",
    "Neck cracking, frequent fatigue, and headaches.": "neck_cracking_fatigue_headaches",
    "Bad sleeping habit.": "bad_sleeping_habit",
    "Over 8 hours of computer use daily.": "computer_over_8h",
    "Frequent neck and shoulder stiffness.": "neck_shoulder_stiffness",
    "Unrefreshing sleep.": "unrefreshing_sleep",
    "Eye strain and chronic headaches.": "eye_strain_headaches"
}

# ✅ 체크리스트 저장
def save_checklist(user_id, factors, all_factors):
    conn = get_connection()
    cur = conn.cursor()
    try:
        kst_now = datetime.utcnow() + timedelta(hours=9)

        # 제출된 값 → DB column 기준으로 정리
        data = {}
        for factor in all_factors:
            column = FACTOR_COLUMNS[factor]
            data[column] = 1 if factor in factors else 0
        data["updated_at"] = kst_now

        # 해당 유저 row 존재 여부 확인
        cur.execute("SELECT user_id FROM checklist WHERE user_id=?", (user_id,))
        exists = cur.fetchone()

        if exists:
            # UPDATE
            set_clause = ", ".join([f"{col}=?" for col in data])
            values = list(data.values()) + [user_id]
            cur.execute(f"""
                UPDATE checklist
                SET {set_clause}
                WHERE user_id=?
            """, values)
        else:
            # INSERT
            columns = ", ".join(["user_id"] + list(data.keys()))
            placeholders = ", ".join(["?"] * (len(data) + 1))
            values = [user_id] + list(data.values())
            cur.execute(f"""
                INSERT INTO checklist ({columns})
                VALUES ({placeholders})
            """, values)

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error saving checklist:", e)
    finally:
        conn.close()

# ✅ 체크리스트 불러오기
def get_user_checklist(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM checklist WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return {}

    # DB column → factor_key 로 매핑
    result = {}
    for factor, column in FACTOR_COLUMNS.items():
        result[factor] = row[column]
    return result

# ✅ 체크리스트 페이지 라우트
@user_service_bp.route("/checklist", methods=["GET", "POST"])
def checklist():
    if "user_id" not in session:
        return redirect(url_for("checklist.guest_checklist"))

    user_id = session["user_id"]

    if request.method == "POST":
        checked_factors = request.form.getlist("factors")
        # 보안 필터링
        checked_factors = [f for f in checked_factors if f in FACTORS]
        save_checklist(user_id, checked_factors, FACTORS)
        return redirect(url_for("checklist.checklist"))

    saved_data = get_user_checklist(user_id)
    return render_template(
        "user_service/checklist.html",
        saved_data=saved_data,
        FACTORS=FACTORS,
        FACTOR_KR=FACTOR_KR
    )

@user_service_bp.route("/stretching")
def stretching():
    return render_template("user_service/stretching.html") 

@user_service_bp.route("/user_service")
def user_service():
    return render_template("user_service/user_service.html")

@user_service_bp.route("/guest_checklist")
def guest_checklist():
    return render_template("user_service/guest_checklist.html")

@user_service_bp.route("/statistics")
def statistics():
    return render_template("user_service/statistics.html")