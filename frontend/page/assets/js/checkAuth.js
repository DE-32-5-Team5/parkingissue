// 인증 상태 확인 함수
async function checkAuth() {
    alert();
    alert("checkAuth.js 실행됨");  // 이 로그를 추가;
    try {
         const token = document.cookie.split('; ').find(row => row.startsWith('jwt_token=')).split('=')[1];  // 쿠키에서 토큰 추출
         const response = await fetch('/api/login/isuser', {
            method: 'POST',  // POST 요청
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,  // Authorization 헤더에 토큰 추가
            },
            credentials: 'include',  // 쿠키 포함 여부
        });
        if (!response.ok) {
            throw new Error('Not authenticated');
        } else {
            window.location.href = '/main';
        }
    } catch (error) {
        // 인증 실패 시 index 페이지로 리디렉션
        window.location.href = '/';
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    checkAuth;
})