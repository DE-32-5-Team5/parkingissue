async function selectNm() {
    // alert("checkAuth.js 실행됨");  // 이 로그를 추가;
    try {
        const response = await fetch('/api2/name', {
            method: 'POST',  // POST 요청
            credentials: 'include',  // 쿠키 자동 포함
            redirect: 'manual',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}), // 빈 데이터 전달
        });

        if (!response.ok) {
            throw new Error('Not authenticated');
        }

        const data = await response.json(); // JSON 파싱
        const namespace = document.getElementById('namespace');
        const profile = document.getElementById('profile-name');
        console.log(data.name[0].manager_company);
        if (data.name && data.name.length > 0) {
            const firstKey = Object.keys(data.name[0])[0]; // 첫 번째 키 가져오기
            const secondKey = Object.keys(data.name[0])[1]; // 두 번째 키 가져오기

            namespace.textContent = data.name[0][firstKey] || '이름 없음';
            profile.textContent = data.name[0][secondKey] || '회사 없음';

        } else {
            namespace.textContent = '이름을 가져올 수 없습니다.';
            profile.textContent = '프로필을 가져올 수 없습니다.';
        }
    } catch (error) {
        // 인증 실패 시 index 페이지로 리디렉션
        alert("로그인 세션이 만료되었습니다.");
        // window.location.href = 'https://parkingissue.online';
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    await selectNm();
});