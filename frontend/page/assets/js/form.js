
// 연관 검색어 데이터 (예시)
// 여기에서는 행사, 맛집 데이터 아래 형식으로 가져오는 쿼리짜면 되고

// const relatedSearches = {
//     '개발': ['개발자 취업', '개발자 로드맵', '개발 공부 방법'],
//     '여행': ['여행지 추천', '여행 준비물', '여행 계획'],
//     '음식': ['음식점 추천', '음식 배달', '음식 레시피']
// };

// 실시간 검색어 데이터 (예시)
// 여기에 log 데이터 긁어오는 쿼리 짜면 되는거고
const trendingSearches = [
    "월드컵 중계",
    "날씨",
    "플레이데이터",
    "만세력",
    "에스파",
    "사주풀이",
    "MBTI",
    "태풍",
    "뉴진즈",
    "아일릿"
];

let selectElementRe = null; // select 요소 가져오기
let selectedValueRe = null;

// 연관검색어 조회용 function
async function relatedSearch(text_value, cls) {
    const url = `https://parkingissue.online/api/getRelated?text=${text_value}&cls=${cls}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store',
        });

        if (!response.ok) {
            throw new Error(`HTTP 오류! 상태: ${response.status}`);
        }

        const data = await response.json();
        // 데이터를 원하는 형식으로 가공
        const relatedSearches = data.reduce((acc, item) => {
            const [key, value] = Object.entries(item)[0];
            if (!acc[key]) {
                acc[key] = [];
            }
            acc[key].push(value);
            return acc;
        }, {});
        return relatedSearches; // 변환된 데이터를 반환
    } catch (error) {
        console.error('연관 검색어 실패:', error);
        return null; // 에러 발생 시 null 반환
    }
}
// 검색어 로그 kafka로 보내기
async function sendSearch(txt_value) {
    const url = `https://parkingissue.online/api/getClickSearch?txt=${txt_value}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store',
        });
        if (!response.ok) {
            throw new Error(`HTTP 오류! 상태: ${response.status}`);
        };
    } catch (error) {
        console.error('카프카 전송 실패:', error);
        return null; // 에러 발생 시 null 반환
    }
}

// DOM 요소
const searchInput = document.querySelector(".search-bar");
const suggestionsDiv = document.querySelector('.suggestions');
const voiceButton = document.querySelector('.voice-search-btn');
const trendingSearchesDiv = document.querySelector('.trending-searches')


let timeout;
let isComposing = false;

searchInput.addEventListener('input', (e) => {
    const value = e.target.value;
    suggestionsDiv.innerHTML = ''; // 기존 제안 목록 초기화
    selectElementRe = document.getElementById("parkhot"); // select 요소 가져오기
    selectedValueRe = selectElementRe.value;
    clearTimeout(timeout); // 이전 타임아웃 제거

    if (value.length > 1) {
        timeout = setTimeout(async () => {
            const relatedSearches = await relatedSearch(value, selectedValueRe);
            // 검색어 카프카로 보내기
            sendSearch(value);
            // const relatedSearches = {
            //     '개발': ['개발자 취업', '개발자 로드맵', '개발 공부 방법'],
            //     '여행': ['여행지 추천', '여행 준비물', '여행 계획'],
            //     '음식': ['음식점 추천', '음식 배달', '음식 레시피']
            // };
            console.log(relatedSearches);
            // 동적으로 input 이벤트가 발생할때마다 해당 단어가 포함된거 찾으면 될듯?
            if (relatedSearches) {
                Object.keys(relatedSearches).forEach(key => {
                    if (key.includes(value)) {
                        relatedSearches[key].forEach(suggestion => {
                            // 제안 항목을 위한 <div> 생성
                            const div = document.createElement('div');
                            div.className = 'suggestion-item';

                            // 제안 텍스트를 위한 <span> 생성
                            const textSpan = document.createElement('span');
                            textSpan.textContent = suggestion;

                            div.appendChild(textSpan);

                            // 클릭 이벤트 핸들러
                            div.onclick = () => {
                                searchInput.value = suggestion;
                                // 클릭한 연관 검색어 카프카로 보내기
                                sendSearch(suggestion);
                                suggestionsDiv.style.display = 'none';
                            };

                            // 제안 목록 컨테이너에 추가
                            suggestionsDiv.appendChild(div);
                        });
                    }
                });
                suggestionsDiv.style.display = 'block'; // 제안 목록 표시
            }
        }, 500); // 1초 지연
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