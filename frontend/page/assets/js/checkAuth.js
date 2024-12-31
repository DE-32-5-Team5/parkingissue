// 인증 상태 확인 함수
async function checkAuth() {
    try {
        const response = await fetch('/protected', { credentials: 'include' });
        if (!response.ok) {
            throw new Error('Not authenticated');
        }
    } catch (error) {
        // 인증 실패 시 index 페이지로 리디렉션
        window.location.href = '/';
    }
}

// 페이지 로드 시 인증 상태 확인
window.onload = checkAuth;