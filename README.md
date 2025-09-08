# Linux 환경에서 GitHub와 연결하여 Push 하기

이 문서는 Linux 환경에서 GitHub 저장소를 SSH로 연결하고, 로컬에서 만든 파일을 원격 저장소로 push하는 과정을 설명합니다.

---

## 1. SSH 키 등록
먼저 로컬 PC(리눅스)와 GitHub를 연결하기 위해 SSH 키를 생성합니다.  
`ssh-keygen` 명령어로 키를 만들고, 공개키(`id_ed25519.pub`)를 GitHub 설정의 **SSH and GPG keys**에 등록합니다.  
이 과정을 거치면 매번 아이디와 비밀번호를 입력하지 않아도 안전하게 연결할 수 있습니다.

---

## 2. 원격 저장소 설정
저장소를 처음 받아올 경우에는 GitHub에서 제공하는 SSH 주소를 이용해 `git clone`을 합니다.  
이미 로컬 저장소가 있다면, 아래와 같이 원격 주소를 SSH 방식으로 변경합니다.

git remote set-url origin git@github.com:USERNAME/REPOSITORY.git

---

## 3. 파일 추가 및 커밋
로컬에서 새로운 파일을 만들거나 기존 파일을 수정한 뒤, Git을 통해 버전 기록을 남깁니다.

git add 파일명 # 변경된 파일을 스테이지에 올림
git commit -m "메시지" # 변경 내용을 커밋으로 기록

커밋은 프로젝트의 히스토리를 남기는 과정으로, push를 하기 위해 반드시 필요합니다.

---

## 4. 원격 저장소로 Push
커밋한 내용을 원격 저장소로 업로드합니다.  
저장소의 기본 브랜치 이름이 `main`이라면:

git push origin main

만약 기본 브랜치가 `master`라면:

git push origin master

---

## 5. 연결 확인
처음 SSH로 GitHub에 접속하면 인증 여부를 확인하는 메시지가 출력됩니다.  
정상적으로 연결되면 다음과 같은 안내가 보입니다.

Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.

---

## ✅ 정리
1. SSH 키 생성 → GitHub에 등록  
2. 원격 저장소를 SSH 주소로 설정  
3. `git add` → `git commit` → `git push` 순서로 업로드  
4. GitHub에서 업로드된 파일 확인  

이 과정을 통해 리눅스 환경에서도 안전하게 GitHub에 프로젝트를 저장하고 관리할 수 있습니다.
