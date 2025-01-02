document.addEventListener("DOMContentLoaded", async function () {
    // 인증 체크 함수
    async function bookmarkCheck(location) {
        try {
            const response = await fetch('/api/bookmark/list', {
                method: 'POST',
                credentials: 'include',  // 쿠키 자동 포함
                redirect: 'manual',
                headers: {
                    'Content-Type': 'application/json', // 수정된 부분
                },
                body: JSON.stringify(location)
            });
            if (!response.ok) {
                throw new Error('Not authenticated');
            }
            const data = await response.json(); // API 응답 데이터
            renderBookmarkList(data.bookmarks); // 북마크 데이터 렌더링
        } catch (error) {
            // 인증 실패 시 index 페이지로 리디렉션
            alert("로그인 세션이 만료되었습니다.");
            window.location.href = 'https://parkingissue.online';
        }
    }

    // 북마크 데이터를 렌더링하는 함수
    function renderBookmarkList(bookmarkList) {
        const bookmarkCardsContainer = document.querySelector('.bookmark-cards');

        // 기존의 카드 초기화
        bookmarkCardsContainer.innerHTML = '';

        if (bookmarkList.length === 0) {
            // 북마크 데이터가 없는 경우 메시지 표시
            const noBookmarkMessage = document.createElement('p');
            noBookmarkMessage.textContent = '즐겨찾기가 없습니다.';
            noBookmarkMessage.style.textAlign = 'center'; // 메시지 가운데 정렬
            noBookmarkMessage.style.color = '#888'; // 메시지 색상 (선택 사항)
            bookmarkCardsContainer.appendChild(noBookmarkMessage);
            return;
        }

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
                <p>현재 위치에서 ${bookmark.distance.toFixed(3)}km</p>
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

    // 현재 위치를 가져오는 함수
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

    const location = await getCurrentLocation();
    await bookmarkCheck(location);
});