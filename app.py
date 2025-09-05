import streamlit as st
import cv2
import mediapipe as mp
import math

# Mediapipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

st.title("실시간 CVA 거북목 측정")

# 웹캠 시작 체크박스
run = st.checkbox("Start Webcam")

# Streamlit에서 영상 표시 공간
FRAME_WINDOW = st.image([])

def calculate_cva_angle(shoulder, ear):
    dx = ear[0] - shoulder[0]
    dy = ear[1] - shoulder[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = abs(angle_rad * 180.0 / math.pi)
    return 90 - angle_deg

if run:
    cap = cv2.VideoCapture(0)
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while run:
            ret, frame = cap.read()
            if not ret:
                st.warning("카메라를 불러올 수 없습니다.")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            h, w, _ = frame.shape

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # 오른쪽 좌표
                shoulder_r = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w),
                              int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h))
                ear_r = (int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x * w),
                         int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y * h))
                
                # 왼쪽 좌표
                shoulder_l = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w),
                              int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h))
                ear_l = (int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x * w),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y * h))

                # CVA 평균
                cva_r = calculate_cva_angle(shoulder_r, ear_r)
                cva_l = calculate_cva_angle(shoulder_l, ear_l)
                cva_avg = abs((cva_r + cva_l) / 2)

                # CVA 표시
                cv2.putText(frame, f"CVA Avg: {cva_avg:.1f} deg", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                # 상태 판정 (30도 기준)
                if cva_avg >= 30:
                    color = (0, 0, 255)
                    status = "Forward Head"
                else:
                    color = (0, 255, 0)
                    status = "Normal"

                cv2.putText(frame, status, (30, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                cv2.line(frame, shoulder_r, ear_r, color, 3)
                cv2.line(frame, shoulder_l, ear_l, color, 3)

                # 랜드마크 그리기
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Streamlit에 프레임 업데이트
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
