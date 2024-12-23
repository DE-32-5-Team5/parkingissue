// Create the event card content and insert it into the #root element
document.addEventListener("DOMContentLoaded", function() {
    const rootElement = document.getElementById("article-section");
  
    const article = document.createElement("article");
    article.classList.add("event-detail");
  
    // Image Section
    const imageContainer = document.createElement("div");
    imageContainer.classList.add("event-image");
    const img = document.createElement("img");
    img.src = "https://images.unsplash.com/photo-1492684223066-81342ee5ff30";
    img.alt = "Coachella Music Festival main stage at sunset";
    imageContainer.appendChild(img);
  
    // Card Content
    const cardContent = document.createElement("div");
    cardContent.classList.add("event-content");
  
    // Title
    const title = document.createElement("h2");
    title.classList.add("title");
    title.textContent = "Coachella Valley Music and Arts Festival 2024";
  
    // Flex Containers for Address, Date, and Phone
    const flexContainers = [
      {
        icon: "📍", // MapPin
        text: "Empire Polo Club, 81-800 Avenue 51, Indio, CA 92201"
      },
      {
        icon: "📅", // Calendar
        text: "April 12-14 & April 19-21, 2024"
      },
      {
        icon: "📞", // Phone
        text: `<a href="tel:+1-855-771-3667">(855) 771-3667</a>`
      }
    ];
  
    flexContainers.forEach(item => {
      const flexDiv = document.createElement("div");
      flexDiv.classList.add("info-item");
  
      const iconSpan = document.createElement("span");
      iconSpan.classList.add("icon");
      iconSpan.textContent = item.icon;
  
      const textSpan = document.createElement("span");
      textSpan.innerHTML = item.text;
  
      flexDiv.appendChild(iconSpan);
      flexDiv.appendChild(textSpan);
  
      cardContent.appendChild(flexDiv);
    });
  
    // Description
    const descriptionSection = document.createElement("div");
    descriptionSection.classList.add("description");
    const descriptionText = document.createElement("p");
    descriptionText.textContent =
      "Experience the world's most iconic music festival featuring top artists, art installations, and unforgettable moments in the California desert.";
  
    descriptionSection.appendChild(descriptionText);
    cardContent.appendChild(descriptionSection);
  
    // Append everything to the article
    article.appendChild(imageContainer);
    article.appendChild(cardContent);
    
    // Append article to the root element
    rootElement.appendChild(article);
});
