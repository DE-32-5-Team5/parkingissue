// script.js

document.addEventListener("DOMContentLoaded", function() {
    // 모든 X 버튼을 찾습니다.
    const closeButtons = document.querySelectorAll('.close-btn');

    // 각 X 버튼에 클릭 이벤트 리스너를 추가합니다.
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 버튼이 속한 부모 요소인 .bookmark-card를 찾고 삭제합니다.
            const card = this.closest('.bookmark-card');
            if (card) {
                card.remove();  // 해당 카드 삭제
            }
        });
    });
});
