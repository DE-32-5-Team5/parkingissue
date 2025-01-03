document.addEventListener("DOMContentLoaded", async function () {
    // 현재 위치 가져오기
    const cen_location = await getCurrentLocation();

    // 연관 검색어 조회 함수
    async function relatedSearch(text_value, cls) {
        const url = `https://parkingissue.online/api/getRelated?text=${text_value}&cls=${cls}&lat=${parseFloat(cen_location.latitude)}&lon=${parseFloat(cen_location.longitude)}`;
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

    // 검색 입력 처리
    const searchInput = document.querySelector(".search-bar");
    const suggestionsDiv = document.querySelector('.suggestions');
    let timeout;

    searchInput.addEventListener('input', (e) => {
        const value = e.target.value;
        suggestionsDiv.innerHTML = ''; // 기존 제안 목록 초기화
        clearTimeout(timeout); // 이전 타임아웃 제거

        if (value.length > 1) {
            timeout = setTimeout(async () => {
                const relatedSearches = await relatedSearch(value, 'hotplace');
                if (relatedSearches) {
                    Object.keys(relatedSearches).forEach(key => {
                        if (key.includes(value)) {
                            relatedSearches[key].forEach(suggestion => {
                                const div = document.createElement('div');
                                div.className = 'suggestion-item';

                                const textSpan = document.createElement('span');
                                textSpan.textContent = suggestion;

                                div.appendChild(textSpan);

                                div.onclick = () => {
                                    searchInput.value = suggestion;
                                    sendSearch(suggestion);
                                    suggestionsDiv.style.display = 'none';
                                };

                                suggestionsDiv.appendChild(div);
                            });
                        }
                    });
                    suggestionsDiv.style.display = 'block'; // 제안 목록 표시
                }
            }, 500); // 500ms 지연
        } else {
            suggestionsDiv.style.display = 'none'; // 입력값 없을 경우 숨기기
        }
    });

    // 검색어 클릭 처리
    suggestionsDiv.addEventListener('click', function (e) {
        if (e.target.classList.contains('suggestion-item')) {
            searchInput.value = e.target.textContent;
            suggestionsDiv.style.display = 'none';
        }
    });

    // 폼 제출 처리
    document.querySelector('.search-form').addEventListener('submit', handleSearch);

    // 검색어 가져오기 함수
    async function getSearchValue() {
        return searchInput.value; // 검색어 값
    }

    // 검색 처리 함수
    async function handleSearch(event) {
        event.preventDefault(); // 기본 폼 제출 동작 방지
        const searchValue = await getSearchValue();

        if (searchValue) {
            console.log("검색어 (Enter 키):", searchValue);
            const enter_result = await performSearch(searchValue);
            if (enter_result) {
                const url = `post1.html?contentid=${enter_result.contentid}`;
                window.location.href = url; // 페이지 이동
            } else {
                alert("검색 결과가 없습니다.");
            }
        } else {
            alert("검색어를 입력하세요.");
        }
    }

    // 실제 검색 동작 (API 호출 또는 데이터 필터링)
    async function performSearch(query) {
        try {
            const response = await fetch(`https://parkingissue.online/api/search?searchWord=${encodeURIComponent(query)}&searchClass=${encodeURIComponent('hotplace')}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                cache: "no-store",
            });
            if (!response.ok) throw new Error(`HTTP error! 상태: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('검색 실패:', error);
            return null;
        }
    }

    // 현재 위치 가져오기 함수
    function getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const { latitude, longitude } = position.coords;
                        console.log(`Current location - Latitude: ${latitude}, Longitude: ${longitude}`); // 로그: 현재 위치
                        resolve({ latitude, longitude });
                    },
                    error => {
                        console.error("Error getting current location:", error);
                        reject(error);
                    }
                );
            } else {
                reject(new Error("Geolocation is not supported by this browser."));
            }
        });
    }
});
