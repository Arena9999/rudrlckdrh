//login_alert
const flashContainer = document.getElementById("flash-container");
if (flashContainer) {
    const messagesData = flashContainer.dataset.messages;
    if (messagesData) {
        const messages = messagesData.split("|");
        messages.forEach(msg => {
            alert(msg);
        });
    }
}



//main_program
document.addEventListener("DOMContentLoaded", async() => {


    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const statusEl = document.getElementById('status');

    function calculateCVA(shoulder, ear) {
        const dx = ear.x - shoulder.x;
        const dy = ear.y - shoulder.y;
        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
        return Math.abs(90 - Math.abs(angle));
    }

    const pose = new Pose({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5/${file}`
    });

    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });

    pose.onResults(onResults);

    // 카메라 스트림 가져오기
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        console.log("카메라 스트림 성공!", stream);
        video.srcObject = stream;
        return video.play();
    })
    .catch(err => console.error("카메라 접근 실패:", err));

    function onResults(results) {
        ctx.save();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        if (results.poseLandmarks) {
            const lm = results.poseLandmarks;
            const shoulder_r = lm[12], ear_r = lm[8];
            const shoulder_l = lm[11], ear_l = lm[7];

            const cva_r = calculateCVA(shoulder_r, ear_r);
            const cva_l = calculateCVA(shoulder_l, ear_l);
            const cva_avg = (cva_r + cva_l) / 2;
            const status = cva_avg >= 25 ? "Forward Head" : "Normal";

            statusEl.innerText = `CVA: ${cva_avg.toFixed(1)}°, 상태: ${status}`;
            ctx.strokeStyle = cva_avg >= 25 ? "red" : "green";
            ctx.beginPath();
            ctx.moveTo(shoulder_r.x*canvas.width, shoulder_r.y*canvas.height);
            ctx.lineTo(ear_r.x*canvas.width, ear_r.y*canvas.height);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(shoulder_l.x*canvas.width, shoulder_l.y*canvas.height);
            ctx.lineTo(ear_l.x*canvas.width, ear_l.y*canvas.height);
            ctx.stroke();
        }
        ctx.restore();
    }

    async function detectPose() {
        await pose.send({ image: video });
        requestAnimationFrame(detectPose);
    }

    video.onloadeddata = () => { detectPose(); };

    const captureBtn = document.getElementById("captureBtn");
    const countdownDisplay = document.getElementById("countdownDisplay");

    if (captureBtn) {
        captureBtn.addEventListener("click", () => {
            let countdown = 3;
            const originalText = statusEl.innerText;

            const interval = setInterval(() => {
                countdownDisplay.innerText = `사진 저장까지 ${countdown}초`;
                countdown--;
                if (countdown < 0) {
                    clearInterval(interval);
                    countdownDisplay.innerText = "";

                    const dataUrl = canvas.toDataURL("image/png");
                    const cvaText = originalText.split("°")[0].replace("CVA: ", "");
                    const statusText = originalText.split("상태: ")[1];

                    fetch("/save", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            cva: parseFloat(cvaText),
                            status: statusText,
                            image: dataUrl
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert("사진 저장 완료!");
                        statusEl.innerText = originalText;
                    })
                    .catch(err => alert("저장 실패"));
                }
            }, 1000);
        });
    }
});
