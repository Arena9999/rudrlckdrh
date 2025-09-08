#세션체크, 로그인, 로그아웃, 회원가입
from account.validators import is_valid_id, is_valid_password
from account.dto import RegexResultDTO
from db import database   # <- 이미 가지고 계신 DB 모듈 불러오기
from werkzeug.security import generate_password_hash
from dataclasses import dataclass

@dataclass
class RegexResultDTO:
    success: bool
    detail: str

def register_user(user_id: str, password: str) -> RegexResultDTO:
    # Step 1. 아이디 검증
    id_result = is_valid_id(user_id)
    if not id_result.success:
        return id_result

    # Step 2. 비밀번호 검증
    pw_result = is_valid_password(password)
    if not pw_result.success:
        return pw_result

    # Step 3. 중복 아이디 확인
    if database.get_user_by_id(user_id):
        return RegexResultDTO(False, "이미 존재하는 아이디입니다.")

    # Step 4. 비밀번호 해싱 후 저장
    hashed_pw = generate_password_hash(password)
    database.add_user(user_id, hashed_pw)

    return RegexResultDTO(True, f"회원가입 성공! 아이디: {user_id}")
