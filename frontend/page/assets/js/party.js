document.addEventListener("DOMContentLoaded", function () {
    const rootElement = document.getElementById("item-container");

    // Generate 23 articles
    for (let i = 0; i < 23; i++) {
        // Wrap entire article content in an <a> tag
        const link = document.createElement("a");
        link.href = "post1.html"; // Link to post1.html
        link.classList.add("article-link");

        const article = document.createElement("article");
        article.classList.add("article");

        // Image Section
        const imageContainer = document.createElement("div");
        imageContainer.classList.add("image-container");
        const img = document.createElement("img");
        img.src = "https://images.unsplash.com/photo-1492684223066-81342ee5ff30";
        img.alt = "Coachella Music Festival main stage at sunset";
        imageContainer.appendChild(img);

        // Card Content
        const cardContent = document.createElement("div");
        cardContent.classList.add("card-content");

        // Title
        const title = document.createElement("h2");
        title.classList.add("card-title");
        title.textContent = "Coachella Valley Music and Arts Festival 2024";

        // Flex Containers for Address and Date
        const flexContainers = [
            {
                iconId: "map-pin",
                icon: "📍", // MapPin
                text: "Empire Polo Club, 81-800 Avenue 51, Indio, CA 92201"
            },
            {
                iconId: "calendar",
                icon: "📅", // Calendar
                text: "April 12-14 & April 19-21, 2024"
            }
        ];

        flexContainers.forEach(item => {
            const flexDiv = document.createElement("div");
            flexDiv.classList.add("flex-container");

            const iconSpan = document.createElement("span");
            iconSpan.classList.add("icon");
            iconSpan.id = item.iconId;
            iconSpan.textContent = item.icon;

            const textSpan = document.createElement("span");
            textSpan.innerHTML = item.text;

            flexDiv.appendChild(iconSpan);
            flexDiv.appendChild(textSpan);

            cardContent.appendChild(flexDiv);
        });

        // Build structure: article -> link -> imageContainer, cardContent
        article.appendChild(imageContainer);
        article.appendChild(cardContent);

        // Add article inside link
        link.appendChild(article);

        // Append link to the root element
        rootElement.appendChild(link);
    }

    // Pagination Variables
    const gallery = document.getElementById("item-container");
    const nextPageButton = document.getElementById("next-page");
    const prevPageButton = document.getElementById("prev-page");

    // Get all item elements
    const items = Array.from(gallery.children);

    let itemsPerPage = getItemsPerPage(); // Initial items per page setting
    let currentPage = 1; // Current page

    // Function to determine items per page based on window size
    function getItemsPerPage() {
        return window.innerWidth <= 768 ? 6 : 9; // 6 items on mobile, 9 items on desktop
    }

    // Function to render the current page
    function renderPage(page) {
        itemsPerPage = getItemsPerPage(); // Dynamically update based on screen size
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        // Hide all items
        items.forEach((item, index) => {
            item.style.display = index >= startIndex && index < endIndex ? "block" : "none";
        });

        // Show/hide pagination buttons
        prevPageButton.style.display = page > 1 ? "inline-block" : "none";
        nextPageButton.style.display = endIndex < items.length ? "inline-block" : "none";
    }

    // Next page button click event
    nextPageButton.addEventListener("click", () => {
        currentPage++;
        renderPage(currentPage);
    });

    // Previous page button click event
    prevPageButton.addEventListener("click", () => {
        currentPage--;
        renderPage(currentPage);
    });

    // Resize event to handle changes in items per page
    window.addEventListener("resize", () => {
        const previousItemsPerPage = itemsPerPage;
        itemsPerPage = getItemsPerPage();

        // Adjust current page if number of items per page changes
        if (itemsPerPage !== previousItemsPerPage) {
            currentPage = Math.ceil((currentPage - 1) * previousItemsPerPage / itemsPerPage) + 1;
        }

        renderPage(currentPage);
    });

    // Initial render
    renderPage(currentPage);
});
