// 검색어 가져오기 함수
function getSearchValue() {
    const searchInput = document.querySelector(".search-bar");
    return searchInput.value.trim(); // 검색어 값 (공백 제거)
}

// Enter 키 입력 또는 검색 버튼 클릭 시 호출되는 함수
function handleSearch(event) {
    event.preventDefault(); // 기본 폼 제출 동작 방지
    const searchValue = getSearchValue();

    if (searchValue) {
        console.log("검색어 (Enter 키):", searchValue);
        // 검색 로직 실행 (예: API 호출)
        performSearch(searchValue);
    } else {
        alert("검색어를 입력하세요.");
    }
}

// 검색 버튼 클릭 시 호출되는 함수
function handleButtonSearch() {
    const searchValue = getSearchValue();

    if (searchValue) {
        console.log("검색어 (검색 버튼):", searchValue);
        // 검색 로직 실행 (예: API 호출)
        performSearch(searchValue);
    } else {
        alert("검색어를 입력하세요.");
    }
}

// 실제 검색 동작 (API 호출 또는 데이터 필터링)
function performSearch(query) {
    console.log(`"${query}"로 검색을 실행합니다.`);
    // 예: 서버로 검색 요청 보내기
    fetch(`https://parkingissue.online/api/search?q=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
        })
        .then(response => response.json())
        .then(data => {
            console.log("검색 결과:", data);
            // 검색 결과를 UI에 렌더링하거나 로직 추가
        })
        .catch(error => console.error("검색 요청 실패:", error));
}
