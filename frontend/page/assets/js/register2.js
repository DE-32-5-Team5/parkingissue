
document.addEventListener("DOMContentLoaded", () => {
    const inputFields = document.querySelectorAll(".form-control"); // 모든 입력 필드 선택

    inputFields.forEach(field => {
        field.addEventListener("input", () => validateField(field)); // 입력 이벤트와 유효성 검사 연결
    });
});

// 입력 필드 유효성 검사 함수
function validateField(field) {
    const value = field.value.trim();

    if (field.id === "password") {
        // 비밀번호 유효성 검증
        const isValid = /^[a-zA-Z][a-zA-Z0-9!@#$%^&*()\-_.+=<>?/]{5,11}$/.test(value);
        toggleValidationClass(field, isValid);
    } else if (field.id === "cid") {
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


// 기업 회원가입 중복확인 버튼 클릭 이벤트
let isIdChecked_E = false;
document.getElementById("c_check-id-btn").addEventListener("click", async () => {
    console.log("중복확인 버튼 클릭됨");
    const companyId = document.getElementById("cid").value;
    console.log("입력한 아이디:", companyId);

    // ID 값이 비어있으면 에러 처리
    if (!companyId) {
        alert("아이디를 입력하세요.");
        return;
    }

    try {
        // FastAPI로 POST 요청
        const response = await fetch("https://parkingissue.online/api/company/check/id", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({id: companyId })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.detail); // 성공 메시지 표시
            isIdChecked_E = true; // 중복확인 완료

        } else {
            const errorData = await response.json();
            alert(errorData.detail); // 에러 메시지 표시
            isIdChecked_E = false; // 중복확인 실패
        }
    } catch (error) {
        console.error("Error during ID check:", error);
        alert("서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.");
    }
});

// 전화번호 중복 체크
let isnumChecked = false;
document.getElementById("num_check-id-btn").addEventListener("click", async () => {
    console.log("중복확인 버튼 클릭됨");
    //const companyId = document.getElementById("cid").value;
    const phone1 = document.getElementById("phone1").value;
    const phone2 = document.getElementById("phone2").value;
    const phone3 = document.getElementById("phone3").value;
    const contact = `${phone1}-${phone2}-${phone3}`;

    console.log("입력한 전화번호:", contact);

    // ID 값이 비어있으면 에러 처리
    if (!phone1 | !phone2 | !phone3) {
        alert("전화번호를 입력하세요.");
        return;
    }

    try {
        // FastAPI로 POST 요청
        const response = await fetch("https://parkingissue.online/api/company/check/phone", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({id: contact })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.detail); // 성공 메시지 표시
            isnumChecked = true; // 중복확인 완료

        } else {
            const errorData = await response.json();
            alert(errorData.detail); // 에러 메시지 표시
            isnumChecked = false; // 중복확인 실패
        }
    } catch (error) {
        console.error("Error during ID check:", error);
        alert("서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.");
    }
});

// 가입하기 버튼
document.getElementById("register-btn").addEventListener("click", async (event) => {
    // 기본 동작(폼 제출)을 막음
    event.preventDefault();

    // 기본 폼 검증 동작 수행
    if (!event.target.form.checkValidity()) {
        event.target.form.reportValidity(); // 브라우저 기본 검증 메시지 표시
        return; // 검증 실패 시 중단
    }

    // 필드 값 가져오기
    const companyName = document.getElementById("companyname").value;
    const manager = document.getElementById("manager").value;
    const contact = `${document.getElementById("phone1").value}-${document.getElementById("phone2").value}-${document.getElementById("phone3").value}`;
    const companyId = document.getElementById("cid").value;
    const companyPw = document.getElementById("password").value;

    // 2. isnumChecked 확인
    if (!isnumChecked) {
        alert("전화번호 중복확인을 해주세요.");
        document.getElementById("phone1").focus();
        return;
    }

    // 3. isIdChecked_E 확인
    if (!isIdChecked_E) {
        alert("아이디 중복확인을 해주세요.");
        document.getElementById("cid").focus();
        return;
    }

    // 4. POST 요청 수행
    try {
        const response = await fetch("https://parkingissue.online/api/company/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                Manager: {
                    company: companyName,
                    name: manager,
                    phone: contact,
                    companyid: companyId,
                    password: companyPw,
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
