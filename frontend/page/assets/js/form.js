
// 연관 검색어 데이터 (예시)
const relatedSearches = {
    '개발': ['개발자 취업', '개발자 로드맵', '개발 공부 방법'],
    '여행': ['여행지 추천', '여행 준비물', '여행 계획'],
    '음식': ['음식점 추천', '음식 배달', '음식 레시피']
};

// 실시간 검색어 데이터 (예시)
const trendingSearches = [
    "월드컵 중계",
    "날씨",
    "코로나 현황",
    "주식",
    "부동산",
    "롤드컵",
    "추석 연휴",
    "태풍",
    "방탄소년단",
    "블랙핑크"
];

// DOM 요소
const searchInput = document.querySelector('.search-bar');
const suggestionsDiv = document.querySelector('.suggestions');
const voiceButton = document.querySelector('.voice-search-btn');
const searchButton = document.querySelector('.search-button');
const trendingSearchesDiv = document.querySelector('.trending-searches')

// 연관 검색어 표시
searchInput.addEventListener('input', (e) => {
    const value = e.target.value;
    suggestionsDiv.innerHTML = ''; // 기존 제안 목록 초기화

    if (value.length > 0) {
        Object.keys(relatedSearches).forEach(key => {
            if (key.includes(value)) {
                relatedSearches[key].forEach(suggestion => {
                    // 제안 항목을 위한 <div> 생성
                    const div = document.createElement('div');
                    div.className = 'suggestion-item';

                    // 아이콘을 위한 <span> 생성
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'suggestion-icon';
                    iconSpan.textContent = '🔍';

                    // 제안 텍스트를 위한 <span> 생성
                    const textSpan = document.createElement('span');
                    textSpan.textContent = suggestion;

                    // 아이콘과 텍스트를 div에 추가
                    div.appendChild(iconSpan);
                    div.appendChild(textSpan);

                    // 클릭 이벤트 핸들러
                    div.onclick = () => {
                        searchInput.value = suggestion;
                        suggestionsDiv.style.display = 'none';
                    };

                    // 제안 목록 컨테이너에 추가
                    suggestionsDiv.appendChild(div);
                });
            }
        });

        suggestionsDiv.style.display = 'block'; // 제안 목록 표시
    } else {
        suggestionsDiv.style.display = 'none'; // 입력값 없을 경우 숨기기
    }
});

// 연관 검색어 클릭 처리
suggestionsDiv.addEventListener('click', function(e) {
    if (e.target.classList.contains('suggestion-item')) {
        searchInput.value = e.target.textContent;
        suggestionsDiv.style.display = 'none';
    }
});

// 음성 검색
voiceButton.addEventListener('click', function() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'ko-KR';
        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
        };

        recognition.onerror = function(event) {
            alert('음성 인식에 실패했습니다. 다시 시도해주세요.');
        };
    } else {
        alert('이 브라우저는 음성 인식을 지원하지 않습니다.');
    }
});

// 실시간 검색어 순위 애니메이션
let currentIndex = 0;
function displayTrendingSearches() {
    const keyword = trendingSearches[currentIndex];
    const div = document.createElement('div');
    div.className = 'trending-item';
    div.textContent = `🔥 ${keyword}`;
    
    trendingSearchesDiv.innerHTML = '';
    trendingSearchesDiv.appendChild(div);
    
    currentIndex = (currentIndex + 1) % trendingSearches.length;
}

// 검색 처리
function handleSearch() {
    const searchTerm = searchInput.value;
    if (searchTerm) {
        alert(`검색어 "${searchTerm}"에 대한 검색을 수행합니다.`);
    }
}
// 페이지 로드 시 실시간 검색어 표시
displayTrendingSearches();

// 클릭 이벤트 처리 (검색창 외부 클릭 시 추천 검색어 숨기기)
document.addEventListener('click', (e) => {
    if (!suggestionsDiv.contains(e.target) && e.target !== searchInput) {
        suggestionsDiv.style.display = 'none';
    }
});

// 실시간 검색어 업데이트 시작
displayTrendingSearches();
setInterval(displayTrendingSearches, 3000);