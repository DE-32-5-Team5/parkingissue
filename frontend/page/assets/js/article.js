document.addEventListener("DOMContentLoaded", async function () {
  console.log("DOM content loaded."); // 로그: DOM 로드 완료

  const rootElement = document.getElementById("article-section");
  const noDataMessage = document.getElementById("no-data-message"); // 데이터 없음 메시지 요소

  // URL 파라미터 가져오기
  const urlParams = new URLSearchParams(window.location.search);
  const contentId = urlParams.get("contentid");

  let items = []; // API로부터 가져온 기사들

  function renderContents(data) {
    console.log(`Rendering articles: ${Array.isArray(data) ? data.length : 1} items`); // 데이터 타입 확인 및 항목 개수 출력
    rootElement.innerHTML = "";
  
    const articles = Array.isArray(data) ? data : [data];
  
    if (articles.length === 0) {
      noDataMessage.style.display = "block";
    } else {
      noDataMessage.style.display = "none";
      articles.forEach((item) => {
        const article = document.createElement("article");
        article.classList.add("event-detail");
  
        const imageContainer = document.createElement("div");
        imageContainer.classList.add("event-image");
        const img = document.createElement("img");
        img.src = item.firstimage2 ? item.firstimage2 : "images/no-photo.jpg";
        img.alt = item.title || "Content image";
        imageContainer.appendChild(img);
  
        const cardContent = document.createElement("div");
        cardContent.classList.add("event-content");

        // ⭐ 버튼 추가
        const bookmarkButton = document.createElement("button");
        bookmarkButton.classList.add("bookmark-button");
        bookmarkButton.textContent = "⭐";
        bookmarkButton.addEventListener("click", async () => {
          try {
            const response = await fetch("/api/bookmark/creation", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ contentid: item.contentid }),
            });

            if (!response.ok) {
              throw new Error(`Bookmark API 요청 실패: ${response.status}`);
            }

            const result = await response.json();
            console.log("Bookmark created:", result); // 성공 메시지 출력
            alert("북마크가 추가되었습니다!"); // 사용자 알림
          } catch (error) {
            console.error("Error creating bookmark:", error);
            alert("북마크 추가 중 문제가 발생했습니다.");
          }
        });
        cardContent.appendChild(bookmarkButton);

        const title = document.createElement("h2");
        title.classList.add("title");
        title.textContent = item.title;

        const flexContainers = [
          { icon: "📍", text: item.title },
          { icon: "📅", text: `${item.eventstartdate} ~ ${item.eventenddate}` },
          { icon: "🌏", text: `<span>${item.address}</span>` },
          { icon: "🔗", text: `<a href="mainpage.html?contentid=${item.contentid}&lat=${item.mapy}&lon=${item.mapx}">지도 바로가기</a>` },
          { icon: "📞", text: item.tel },
        ];

        const descriptionSection = document.createElement("div");
        descriptionSection.classList.add("description");
        const descriptionText = document.createElement("p");
        descriptionText.textContent = item.description;

        flexContainers.forEach((container) => {
          const flexDiv = document.createElement("div");
          flexDiv.classList.add("info-item");

          const iconSpan = document.createElement("div");
          iconSpan.classList.add("icon");
          iconSpan.textContent = container.icon;

          const textSpan = document.createElement("div");
          textSpan.classList.add("text-space");
          textSpan.innerHTML = container.text;

          flexDiv.appendChild(iconSpan);
          flexDiv.appendChild(textSpan);

          cardContent.appendChild(flexDiv);
        });

        descriptionSection.appendChild(descriptionText);
        cardContent.appendChild(descriptionSection);

        article.appendChild(imageContainer);
        article.appendChild(cardContent);

        rootElement.appendChild(article);
      });
    }
  }

  async function fetchData(apiEndpoint) {
    console.log("Fetching data from API...");
    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        throw new Error(`API 요청 실패: ${response.status}`);
      }

      const data = await response.json();
      console.log("Data fetched from API:", data);
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      return [];
    }
  }

  const apiEndpoint = `https://parkingissue.online/api/hotplace/content?contentid=${contentId}`;

  items = await fetchData(apiEndpoint);
  renderContents(items);
  
  // CSS 스타일 동적으로 추가
  const style = document.createElement("style");
  style.textContent = `
    .bookmark-button {
      position: absolute;
      top: -20px; /* 20px 위로 이동 */
      right: 10px; /* 오른쪽 정렬 */
      width: 40px; /* 버튼의 너비 */
      height: 40px; /* 버튼의 높이 */
      background-color: white; /* 동그라미 배경색 */
      border: 2px solid #ccc; /* 동그라미 테두리 */
      border-radius: 50%; /* 동그라미 모양 */
      display: flex; /* 가운데 정렬을 위해 flex 사용 */
      align-items: center; /* 세로 가운데 정렬 */
      justify-content: center; /* 가로 가운데 정렬 */
      font-size: 24px; /* 별 크기 */
      cursor: pointer; /* 클릭 가능한 커서 */
      z-index: 100; /* 다른 요소 위로 나오도록 설정 */
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 약간의 그림자 추가 */
    }
    .bookmark-button:hover {
      // background: orange;
    }
    .event-content {
      position: relative;
      // padding: 20px;
      border: 1px solid #ddd;
      border-radius: 10px;
    }
  `;
  document.head.appendChild(style);
});
