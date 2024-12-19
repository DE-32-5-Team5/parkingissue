document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM content loaded."); // 로그: DOM 로드 완료

    const rootElement = document.getElementById("item-container");
    const nextPageButton = document.getElementById("next-page");
    const prevPageButton = document.getElementById("prev-page");
    const loader = document.getElementById("loader");
    const noDataMessage = document.getElementById("no-data-message"); // 데이터 없음 메시지 요소
    let items = []; // Articles from API
    let itemsPerPage = getItemsPerPage(); // Initial items per page setting
    let currentPage = 1; // Current page

    console.log(`Initial itemsPerPage: ${itemsPerPage}`); // 로그: 초기 itemsPerPage

    // Function to determine items per page based on window size
    function getItemsPerPage() {
        const count = window.innerWidth <= 768 ? 6 : 9; // 6 items on mobile, 9 items on desktop
        console.log(`Determined itemsPerPage based on window size: ${count}`); // 로그: itemsPerPage 결정
        return count;
    }

    // Function to render articles
    function renderArticles(data) {
        console.log(`Rendering articles: ${data.length} items`); // 로그: 렌더링할 항목 개수
        rootElement.innerHTML = ""; // Clear container

        if (data.length === 0) {
            // 데이터가 없으면 예시 메시지 표시
            noDataMessage.style.display = "block";
        } else {
            noDataMessage.style.display = "none"; // 데이터가 있으면 예시 메시지 숨기기
            data.forEach((item, index) => {
                console.log(`Rendering article #${index + 1}:`, item); // 로그: 각 항목 정보

                const link = document.createElement("a");
                link.href = item.link; // Dynamic link
                link.classList.add("article-link");

                const article = document.createElement("article");
                article.classList.add("article");

                // Image Section
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");
                const img = document.createElement("img");
                img.src = item.image; // Dynamic image
                img.alt = item.alt || "Article image";
                imageContainer.appendChild(img);

                // Card Content
                const cardContent = document.createElement("div");
                cardContent.classList.add("card-content");

                // Title
                const title = document.createElement("h2");
                title.classList.add("card-title");
                title.textContent = item.title; // Dynamic title

                // Flex Containers for Address and Date
                const flexContainers = [
                    {
                        iconId: "map-pin",
                        icon: "📍",
                        text: item.location // Dynamic location
                    },
                    {
                        iconId: "calendar",
                        icon: "📅",
                        text: item.date // Dynamic date
                    }
                ];

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

                // Build structure
                article.appendChild(imageContainer);
                article.appendChild(cardContent);
                link.appendChild(article);
                rootElement.appendChild(link);
            });
        }
    }

    // Function to render the current page
    function renderPage(page) {
        console.log(`Rendering page ${page}`); // 로그: 현재 페이지
        itemsPerPage = getItemsPerPage(); // Dynamically update based on screen size
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        console.log(`Page range: ${startIndex} to ${endIndex - 1}`); // 로그: 페이지 범위
        const paginatedItems = items.slice(startIndex, endIndex);

        // Render paginated items
        renderArticles(paginatedItems);

        // Show/hide pagination buttons
        prevPageButton.style.display = page > 1 ? "inline-block" : "none";
        nextPageButton.style.display = endIndex < items.length ? "inline-block" : "none";

        console.log(`Pagination buttons - Prev: ${prevPageButton.style.display}, Next: ${nextPageButton.style.display}`); // 로그: 페이지 버튼 상태
    }

    // Fetch data from API
    async function fetchData(apiEndpoint, requestData) {
        console.log("Fetching data from API..."); // 로그: API 데이터 가져오기 시작
        loader.style.display = "block";

        try {
            const response = await fetch(apiEndpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
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

    // Function to handle filter actions
    async function handleFilter(filterType) {
        let apiEndpoint;
        let requestData = {};

        switch (filterType) {
            case "default":
                apiEndpoint = "/api/hotplace/list/default";
                requestData = { longitude: 127.1, latitude: 37.5 }; // 사용자 위치
                break;
            case "ongoing":
                apiEndpoint = "/api/hotplace/list/ongoing";
                break;
            case "upcoming":
                apiEndpoint = "/api/hotplace/list/upcoming";
                break;
            case "address":
                apiEndpoint = "/api/hotplace/list/address";
                requestData = { region: "Seoul" }; // 예시: 지역 이름
                break;
            default:
                console.error("Unknown filter type");
                return;
        }

        items = await fetchDataWithLoading(apiEndpoint, requestData);

        // 데이터 매핑
        const mappedItems = items.map((item) => ({
            title: item.title,
            link: "post1.html", // 링크 정보 필요
            image: item.firstimage,
            alt: item.title,
            location: `${item.mapx}, ${item.mapy}`, // 지도 좌표
            date: `${item.eventstartdate} ~ ${item.eventenddate}`
        }));

        currentPage = 1; // 페이지 초기화
        renderPage(currentPage);
    }

    // Fetch data with loading
    async function fetchDataWithLoading(apiEndpoint, requestData) {
        const loader = document.getElementById("loader"); // 로딩 UI 요소
        loader.style.display = "block";

        const data = await fetchData(apiEndpoint, requestData);

        loader.style.display = "none";
        return data;
    }

    // Event listeners for pagination
    nextPageButton.addEventListener("click", () => {
        console.log("Next page button clicked."); // 로그: 다음 페이지 버튼 클릭
        currentPage++;
        renderPage(currentPage);
    });

    prevPageButton.addEventListener("click", () => {
        console.log("Previous page button clicked."); // 로그: 이전 페이지 버튼 클릭
        currentPage--;
        renderPage(currentPage);
    });

    // Resize event to handle changes in items per page
    window.addEventListener("resize", () => {
        console.log("Window resized."); // 로그: 창 크기 조정
        const previousItemsPerPage = itemsPerPage;
        itemsPerPage = getItemsPerPage();

        if (itemsPerPage !== previousItemsPerPage) {
            console.log(`Items per page changed from ${previousItemsPerPage} to ${itemsPerPage}`); // 로그: itemsPerPage 변경
            currentPage = Math.ceil((currentPage - 1) * previousItemsPerPage / itemsPerPage) + 1;
        }

        renderPage(currentPage);
    });

    // Initial API call and setup
    const apiEndpoint = "/api/hotplace/list/default";
    const requestData = { longitude: 127.1, latitude: 37.5 }; // 사용자 위치

    items = await fetchData(apiEndpoint, requestData);
    renderPage(currentPage);

    // 예시 필터 적용
    handleFilter("default"); // 기본 필터 적용
});
