async function checkAuth() {
    // alert("checkAuth.js 실행됨");  // 이 로그를 추가;
    try {
        const response = await fetch('/api/login/isuser', {
            method: 'POST',  // POST 요청
            credentials: 'include',  // 쿠키 자동 포함
            redirect: 'manual',
        });
        if (!response.ok) {
            throw new Error('Not authenticated');
        }
    } catch (error) {
        // 인증 실패 시 index 페이지로 리디렉션
        alert("로그인 세션이 만료되었습니다.");
        window.location.href = 'https://parkingissue.online';
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    checkAuth();
});