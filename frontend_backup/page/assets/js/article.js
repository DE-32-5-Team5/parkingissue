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
  
    // 데이터를 배열로 변환
    const articles = Array.isArray(data) ? data : [data];
  
    if (articles.length === 0) {
      noDataMessage.style.display = "block";
    } else {
      noDataMessage.style.display = "none";
      articles.forEach((item) => {
        const article = document.createElement("article");
        article.classList.add("event-detail");
  
        // 이미지 부분
        const imageContainer = document.createElement("div");
        imageContainer.classList.add("event-image");
        const img = document.createElement("img");
        img.src = item.firstimage2 ? item.firstimage2 : "images/no-photo.jpg";
        img.alt = item.title || "Content image";
        imageContainer.appendChild(img);
  
        // 카드 컨텐츠 생성
        const cardContent = document.createElement("div");
        cardContent.classList.add("event-content");
  
        // 제목 생성
        const title = document.createElement("h2");
        title.classList.add("title");
        title.textContent = item.title;
  
        // 내용물
        const flexContainers = [
          {
            icon: "📍", // title
            text: item.title,
          },
          {
            icon: "📅", // eventstartdate ~ eventenddate
            text: `${item.eventstartdate} ~ ${item.eventenddate}`,
          },
          {
            icon: "🌏", // address
            text: item.address,
          },
          {
            icon: "📞", // tel
            text: item.tel,
          },
        ];
  
        // 설명 부분
        const descriptionSection = document.createElement("div");
        descriptionSection.classList.add("description");
        const descriptionText = document.createElement("p");
        descriptionText.textContent = item.description;
  
        flexContainers.forEach((container) => {
          const flexDiv = document.createElement("div");
          flexDiv.classList.add("info-item");
  
          const iconSpan = document.createElement("span");
          iconSpan.classList.add("icon");
          iconSpan.textContent = container.icon;
  
          const textSpan = document.createElement("span");
          textSpan.innerHTML = container.text;
  
          flexDiv.appendChild(iconSpan);
          flexDiv.appendChild(textSpan);
  
          cardContent.appendChild(flexDiv);
        });
  
        // 컨텐츠 생성
        descriptionSection.appendChild(descriptionText);
        cardContent.appendChild(descriptionSection);
  
        // Append everything to the article
        article.appendChild(imageContainer);
        article.appendChild(cardContent);
  
        // Append article to the root element
        rootElement.appendChild(article);
      });
    }
  }
  

  // Fetch data from API
  async function fetchData(apiEndpoint) {
      console.log("Fetching data from API..."); // 로그: API 데이터 가져오기 시작

      try {
          const response = await fetch(apiEndpoint, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
          });

          if (!response.ok) {
              throw new Error(`API 요청 실패: ${response.status}`);
          }

          const data = await response.json();
          console.log("Data fetched from API:", data); // 로그: API 데이터 가져오기 완료
          return data;
      } catch (error) {
          console.error("Error fetching data:", error);
          return [];
      }
  }

  // 엔드포인트
  const apiEndpoint = `https://parkingissue.online/api/hotplace/content?contentid=${contentId}`;

  // 데이터 가져오기 및 렌더링
  items = await fetchData(apiEndpoint);
  renderContents(items);
});
