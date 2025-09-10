// 메인 페이지 - 동영상 버튼 클릭 시 알림
document.addEventListener("DOMContentLoaded", function () {
    const playBtn = document.querySelector(".play-btn");
    if (playBtn) {
        playBtn.addEventListener("click", function () {
            alert("데모 영상을 재생합니다! (실제로는 영상 연결 가능)");
        });
    }
});


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
