document.addEventListener("DOMContentLoaded", async function () {
  console.log("DOM content loaded.");

  const rootElement = document.getElementById("article-section");
  const noDataMessage = document.getElementById("no-data-message");

  const urlParams = new URLSearchParams(window.location.search);
  const contentId = urlParams.get("contentid");

  let items = [];

  function renderContents(data, checkResult) {
    console.log(`Rendering articles: ${Array.isArray(data) ? data.length : 1} items`);
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

        const bookmarkButton = document.createElement("button");
        bookmarkButton.classList.add("bookmark-button");

        const img2 = document.createElement("img");
        img2.src = checkResult.isitbookmarked
          ? "images/free-icon-favorite-2550357.png"
          : "images/free-icon-star-5708819.png";
        img2.alt = "bookmark star image By rizky adhitya pradana";

        bookmarkButton.addEventListener("click", async () => {
          try {
            const response = await bookmarkCheck(contentId);

            img2.src = response.creation === "true"
              ? "images/free-icon-favorite-2550357.png"
              : "images/free-icon-star-5708819.png";

          } catch (error) {
            console.error("Error updating bookmark:", error);
          }
        });

        bookmarkButton.appendChild(img2);
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
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();
      console.log("Data fetched from API:", data);
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      return [];
    }
  }

  async function bookmarkCheck(contentId) {
    try {
      const response = await fetch('/api/bookmark/creation', {
        method: 'POST',
        credentials: 'include',
        redirect: 'manual',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contentid: contentId
        }),
      });

      if (!response.ok) {
        throw new Error('Not authenticated');
      }

      return await response.json();
    } catch (error) {
      alert("즐겨찾기에 실패하였습니다.");
      throw error;
    }
  }

  const apiEndpoint = `https://parkingissue.online/api/hotplace/content?contentid=${contentId}`;

  async function checkResponse(contentId) {
  try {
    const response = await fetch('/api/bookmark/check', {
      method: 'POST',
      credentials: 'include',
      redirect: 'manual',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contentid: contentId
      }),
    });

    if (!response.ok) {
      throw new Error('Not authenticated');
    }

    return await response.json();
   } catch (error) {
    alert("즐겨찾기에 실패하였습니다.");
    throw error;
    }
 }

  items = await fetchData(apiEndpoint);
  checkResult = await checkResponse(contentId);
  renderContents(items, checkResult);

  const style = document.createElement("style");
  style.textContent = `
    .bookmark-button {
      position: absolute;
      top: 20px;
      right: 10px;
      width: 40px;
      height: 40px;
      border: 2px solid #ccc;
      border-radius: 0%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      cursor: pointer;
      z-index: 100;
    }
    .bookmark-button img {
      max-width: 100%;
      max-height: 100%;
      height: auto;
      width: auto;
    }
    .event-content {
      position: relative;
      border: 1px solid #ddd;
      border-radius: 10px;
    }
    @media (max-width: 767px) {
      .bookmark-button {
        top: 10px;
        width: 20px;
        height: 20px;
      }
    }
  `;
  document.head.appendChild(style);
});