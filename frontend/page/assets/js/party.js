document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM content loaded."); // 로그: DOM 로드 완료

    const rootElement = document.getElementById("item-container");
    const loader = document.getElementById("loader");
    const noDataMessage = document.getElementById("no-data-message"); // 데이터 없음 메시지 요소
    let items = []; // API로부터 가져온 기사들
    let itemsPerPage = getItemsPerPage(); // 페이지당 항목 수
    let currentPage = 1; // 현재 페이지
    let totalPages = 1; // 전체 페이지 수

    console.log(`Initial itemsPerPage: ${itemsPerPage}`); // 로그: 초기 itemsPerPage

    // 화면 크기에 따라 한페이지에 보일 총 아이템의 개수
    function getItemsPerPage() {
        const count = window.innerWidth <= 768 ? 6 : 9; // 모바일에서는 6개, 데스크탑에서는 9개
        console.log(`Determined itemsPerPage based on window size: ${count}`); // 로그: itemsPerPage 결정
        return count;
    }

    // 게시글 랜더링
    function renderArticles(data) {
        console.log(`Rendering articles: ${data.length} items`); // 로그: 렌더링할 항목 개수
        rootElement.innerHTML = ""; // Clear container

        if (data.length === 0) {
            noDataMessage.style.display = "block"; // 데이터가 없으면 메시지 표시
        } else {
            noDataMessage.style.display = "none"; // 데이터가 있으면 메시지 숨김
            data.forEach((item, index) => {
                console.log(`Rendering article #${index + 1}:`, item); // 로그: 각 항목 정보

                const link = document.createElement("a");
                link.href = "post1.html"; // 파일 링크 설정
                link.id = item.contentid; // 컨텐츠 아이디값
                link.addEventListener("click", (e) => {
                    e.preventDefault(); // 기본 동작 방지
                    const contentId = link.id;
                    window.location.href = `post1.html?contentid=${contentId}`;
                });
                link.classList.add("article-link");

                const article = document.createElement("article");
                article.classList.add("article");

                // 이미지 부분
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");
                const img = document.createElement("img");
                img.src = item.firstimage ? item.firstimage : "images/no-photo.jpg";
                img.alt = item.title || "Article image";
                imageContainer.appendChild(img);

                // 카드 컨텐츠 생성
                const cardContent = document.createElement("div");
                cardContent.classList.add("card-content");

                // 제목 생성
                const title = document.createElement("h2");
                title.classList.add("card-title");
                title.textContent = item.title; // 제목 연결

                // 내용물
                const flexContainers = [
                    { iconId: "map-pin", icon: "📍", text: item.title },
                    { iconId: "calendar", icon: "📅", text: item.eventstartdate + '  ~  ' + item.eventenddate }
                ];
                
                // 카드 컨텐츠 붙이기
                flexContainers.forEach(flexItem => {
                    const flexDiv = document.createElement("div");
                    flexDiv.classList.add("flex-container");

                    const iconSpan = document.createElement("span");
                    iconSpan.classList.add("icon");
                    iconSpan.id = flexItem.iconId;
                    iconSpan.textContent = flexItem.icon;

                    const textSpan = document.createElement("span");
                    textSpan.innerHTML = flexItem.text;

                    flexDiv.appendChild(iconSpan);
                    flexDiv.appendChild(textSpan);

                    cardContent.appendChild(flexDiv);
                });

                // 게시글 생성
                article.appendChild(imageContainer);
                article.appendChild(cardContent);
                link.appendChild(article);
                rootElement.appendChild(link);
            });
        }
    }

    // 현재 페이지 랜더링
    function renderPage(page) {
        console.log(`Rendering page ${page}`); // 로그: 현재 페이지
        itemsPerPage = getItemsPerPage(); // 스크린 사이즈에 맞는 컨텐츠 갯수 생성
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        console.log(`Page range: ${startIndex} to ${endIndex - 1}`); // 로그: 페이지 범위
        console.log(typeof(items))
        console.log(items)
        const paginatedItems = items.slice(startIndex, endIndex);

        renderArticles(paginatedItems);

        const paginationContainer = document.getElementById("pagination");
        paginationContainer.innerHTML = ""; // 기존 페이지 버튼들 초기화

        // 페이지 번호 동적 생성
        totalPages = Math.ceil(items.length / itemsPerPage);
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement("button");
            pageButton.textContent = i;
            pageButton.classList.add("page-button");
            pageButton.addEventListener("click", () => {
                currentPage = i;
                renderPage(currentPage);
            });
            paginationContainer.appendChild(pageButton);
        }

        // 페이지 버튼 표시 여부
        paginationContainer.style.display = totalPages > 1 ? "flex" : "none";

        console.log(`Pagination buttons created. Total pages: ${totalPages}`);
    }

    // Fetch data from API
    async function fetchData(apiEndpoint, requestData) {
        console.log("Fetching data from API..."); // 로그: API 데이터 가져오기 시작
        loader.style.display = "block";

        try {
            const response = await fetch(apiEndpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`API 요청 실패: ${response.status}`);
            }

            const data = await response.json();
            console.log("Data fetched from API:", data); // 로그: API 데이터 가져오기 완료
            loader.style.display = "none";
            return data;
        } catch (error) {
            console.error("Error fetching data:", error);
            loader.style.display = "none";
            return [];
        }
    }

    // Get current location
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

    // Handle filter actions
    async function handleFilter(filterType) {
        console.log(`handleFilter called with filterType: ${filterType}`); // 디버깅: filterType 출력
        let apiEndpoint;
        let requestData = {};

        switch (filterType) {
            case "default":
                const location = await getCurrentLocation();
                apiEndpoint = "https://parkingissue.online/api/hotplace/list/default";
                requestData = { latitude: parseFloat(location.latitude), longitude: parseFloat(location.longitude) };
                break;
            case "ongoing":
                apiEndpoint = "https://parkingissue.online/api/hotplace/list/ongoing";
                break;
            case "upcoming":
                apiEndpoint = "https://parkingissue.online/api/hotplace/list/upcoming";
                break;
            default:
                console.error("Unknown filter type");
                return;
        }

        items = await fetchDataWithLoading(apiEndpoint, requestData);

        currentPage = 1;
        renderPage(currentPage);
    }

    async function fetchDataWithLoading(apiEndpoint, requestData) {
        loader.style.display = "block";
        const data = await fetchData(apiEndpoint, requestData);
        loader.style.display = "none";
        return data;
    }

    // Initial filter to load data
    handleFilter("default");

    //
    const filterSelect = document.getElementById("select");
    filterSelect.addEventListener("change", async function () {
        const selectedFilter = filterSelect.value;
        console.log("******************")
        console.log(selectedFilter)
        console.log("******************")
        await handleFilter(selectedFilter);
    })
    
});
