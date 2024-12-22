// 음성 검색 버튼 클릭 이벤트
const voiceSearchBtn = document.querySelector('.voice-search-btn');
const searchBar = document.querySelector('.search-bar');

// 음성 검색 시간 제한 설정 (초 단위)
const TIME_LIMIT_SECONDS = 5;

voiceSearchBtn.addEventListener('click', () => {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'ko-KR'; // 한국어로 설정
        recognition.interimResults = false;

        let timeoutId;

        recognition.onstart = () => {
            console.log('음성 인식 시작');
            // 시간 제한 후 자동 종료
            timeoutId = setTimeout(() => {
                recognition.stop();
                console.log('음성 인식 시간 초과로 종료');
            }, TIME_LIMIT_SECONDS * 1000); // 밀리초 단위 변환
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('음성 인식 결과:', transcript);
            // 음성 인식 결과를 검색창에 넣음
            searchBar.value = transcript;
        };

        recognition.onerror = (event) => {
            console.error('음성 인식 오류:', event.error);
        };

        recognition.onend = () => {
            console.log('음성 인식 종료');
            // 시간 초과 타이머 초기화
            clearTimeout(timeoutId);
        };

        recognition.start();
    } else {
        alert('이 브라우저는 음성 인식을 지원하지 않습니다.');
    }
});
