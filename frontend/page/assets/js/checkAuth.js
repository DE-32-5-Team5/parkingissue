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

        // 응답을 JSON으로 변환
        const data = await response.json();

        // 응답 데이터가 배열 형식인지 확인
        if (Array.isArray(data) && data.length > 0) {
            const userType = data[0]; // 0번 인덱스의 값
            const idvalue = data[1];
            alert(userType);
            const mypageLink = document.getElementById('mypage'); // mypage ID를 가진 a 태그 선택
            const ID = document.getElementById('ID');
            if (ID) {
                ID.textContent = idvalue;
            }
            // userType에 따라 href 경로 설정
            if (mypageLink) {
                if (userType === 1) {
                    mypageLink.href = 'personal_mypage.html';
                } else if (userType === 2) {
                    mypageLink.href = 'enterprise_mypage.html';
                }
            }
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