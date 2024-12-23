// 입력 필드 유효성 검사 함수
function validateField(field) {
    const value = field.value.trim();

    if (field.id === "nickname") {
        // 닉네임 유효성 검증
        const isValid = /^[a-zA-Z가-힣][a-zA-Z가-힣0-9]{1,11}$/.test(value);
        toggleValidationClass(field, isValid);
    } else if (field.id === "password") {
        // 비밀번호 유효성 검증
        const isValid = /^[a-zA-Z][a-zA-Z0-9!@#$%^&*()\-_.+=<>?/]{5,11}$/.test(value);
        toggleValidationClass(field, isValid);
    } else if (field.id === "id") {
        // 아이디 유효성 검증
        const isValid = /^[a-zA-Z][a-zA-Z0-9]{5,19}$/.test(value);
        toggleValidationClass(field, isValid);
    }
}

// 유효성 검증 결과에 따라 클래스 토글
function toggleValidationClass(field, isValid) {
    if (isValid) {
        field.classList.add("valid");
        field.classList.remove("invalid");
    } else {
        field.classList.add("invalid");
        field.classList.remove("valid");
    }
}

// 이벤트 리스너 추가: input과 textarea 모두 선택
document.querySelectorAll("input, textarea").forEach(field => {
    field.addEventListener("input", () => validateField(field));
});


let isIdChecked = false; // 중복확인 여부 추적

document.getElementById("check-id-btn").addEventListener("click", async () => {
    const userId = document.getElementById("id").value;

    // ID 값이 비어있으면 에러 처리
    if (!userId) {
        alert("아이디를 입력하세요.");
        return;
    }

    try {
        // FastAPI로 POST 요청
        const response = await fetch("https://parkingissue.online/api/users/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({id: userId })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.detail); // 성공 메시지 표시
            isIdChecked = true; // 중복확인 완료

        } else {
            const errorData = await response.json();
            alert(errorData.detail); // 에러 메시지 표시
            isIdChecked = false; // 중복확인 실패
        }
    } catch (error) {
        console.error("Error during ID check:", error);
        alert("서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.");
    }
});


// 가입하기 버튼 클릭 이벤트
document.getElementById("register-btn").addEventListener("click", async (event) => {
        // 기본 동작(폼 제출)을 막음
    event.preventDefault();
    const userName = document.getElementById("username").value;
    const userNick = document.getElementById("nickname").value;
    const userId = document.getElementById("id").value;
    const userPw = document.getElementById("password").value;

    if (!isIdChecked) {
        alert("아이디 중복확인을 해주세요.");
        document.getElementById("id").focus();
        return;
        
    }

    try {
        const response = await fetch("https://parkingissue.online/api/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                User: {
                    userName: userName,
                    userNick: userNick,
                    userId: userId,
                    userPw: userPw,
                },
            }),
        });

        if (response.ok) {
            const data = await response.json();
            alert("회원가입이 성공적으로 완료되었습니다!");
            window.location.href = "https://parkingissue.online/"; 
        } else {
            const errorData = await response.json();
            alert(`회원가입 실패: ${errorData.detail}`);
        }
    } catch (error) {
        console.error("Error during registration:", error);
        alert("서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.");
    }
});

