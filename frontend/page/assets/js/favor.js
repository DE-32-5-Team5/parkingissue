document.addEventListener("DOMContentLoaded", async function () {
    // 북마크 데이터를 렌더링하는 함수
    function renderBookmarkList(bookmarkList) {
        const bookmarkCardsContainer = document.querySelector('.bookmark-cards');

        // 기존의 카드 초기화
        bookmarkCardsContainer.innerHTML = '';

        // 북마크 데이터를 순회하며 카드 생성
        bookmarkList.forEach(bookmark => {
            const card = document.createElement('div');
            card.classList.add('bookmark-card');

            card.innerHTML = `
                <div class="flag-icon">
                    <i class="fas fa-flag" style="color: white;"></i>
                </div>
                <h3>${bookmark.title}</h3>
                <p>${bookmark.address}</p>
                <p>현재 위치에서 ${bookmark.distance}km</p>
                <div class="close-btn">
                    <i class="fas fa-times"></i> <!-- X 아이콘 -->
                </div>
            `;

            // 카드 삭제 버튼 이벤트 추가
            const closeButton = card.querySelector('.close-btn');
            closeButton.addEventListener('click', function () {
                card.remove();
            });

            bookmarkCardsContainer.appendChild(card);
        });
    }

    try {
        // 북마크 데이터 요청
        const response = await fetch('/api/bookmark/list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: "Sample Title", // 예시 데이터
                idtype: "SampleType",
                idcode: "SampleCode",
                mapx: 127.0,
                mapy: 37.0
            })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch bookmark list');
        }

        const data = await response.json(); // API 응답 데이터
        renderBookmarkList(data.bookmarks); // 북마크 데이터 렌더링
    } catch (error) {
        console.error('Error fetching bookmark data:', error);
    }
});
