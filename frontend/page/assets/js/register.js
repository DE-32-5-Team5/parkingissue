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




// document.addEventListener('DOMContentLoaded', () => {
//     const userForm = document.querySelector('.formAll');
//     const companyForm = document.querySelector('.formAllC');
    
//     // 개인 폼 아이디 체크
//     const userIdInput = document.getElementById('id');
//     userIdInput.addEventListener('input', () => {
//         const userId = userIdInput.value;
//         if (userId.length >= 6) {
//             checkUserId(userId);
//         }
//     });

//     // 기업 폼 아이디 체크
//     const companyIdInput = document.getElementById('id');
//     companyIdInput.addEventListener('input', () => {
//         const companyId = companyIdInput.value;
//         if (companyId.length >= 6) {
//             checkManagerId(companyId);
//         }
//     });

//     // 회원가입 버튼 클릭 시
//     userForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         const userData = {
//             name: document.getElementById('username').value,
//             nickname: document.getElementById('nickname').value,
//             id: document.getElementById('id').value,
//             password: document.getElementById('password').value
//         };
//         registerUser(userData);
//     });

//     companyForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         const companyData = {
//             company: document.getElementById('username').value,
//             managerName: document.getElementById('id').value,
//             phone: document.getElementById('phone1').value + document.getElementById('phone2').value + document.getElementById('phone3').value,
//             id: document.getElementById('id').value,
//             password: document.getElementById('password').value
//         };
//         registerManager(companyData);
//     });

//     // 아이디 체크 - 개인
//     function checkUserId(userId) {
//         const regex = /^[a-zA-Z][a-zA-Z0-9]{5,19}$/; // 6~20자, 첫번째는 알파벳, 숫자 가능
//         if (!regex.test(userId)) {
//             userIdInput.value = '';
//             userIdInput.placeholder = '아이디는 6~20자, 첫 자는 영어로 시작해야 합니다.';
//             userIdInput.style.color = 'red';
//         } else {
//             // 유효한 아이디 형식인 경우 서버로 요청
//             fetch(`/api/users/check`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ User: { id: userId } }),
//             }).then(response => response.json())
//               .then(data => {
//                   if (data.status !== 200) {
//                       userIdInput.value = '';
//                       userIdInput.placeholder = data.detail;
//                       userIdInput.style.color = 'red';
//                   }
//               });
//         }
//     }

//     // 아이디 체크 - 기업
//     function checkManagerId(managerId) {
//         const regex = /^[a-zA-Z][a-zA-Z0-9]{5,19}$/; // 6~20자, 첫번째는 알파벳, 숫자 가능
//         if (!regex.test(managerId)) {
//             companyIdInput.value = '';
//             companyIdInput.placeholder = '아이디는 6~20자, 첫 자는 영어로 시작해야 합니다.';
//             companyIdInput.style.color = 'red';
//         } else {
//             // 유효한 아이디 형식인 경우 서버로 요청
//             fetch(`/api/company/check/id`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ Manager: { id: managerId } }),
//             }).then(response => response.json())
//               .then(data => {
//                   if (data.status !== 200) {
//                       companyIdInput.value = '';
//                       companyIdInput.placeholder = data.detail;
//                       companyIdInput.style.color = 'red';
//                   }
//               });
//         }
//     }

//     // 회원가입 - 개인
//     function registerUser(userData) {
//         const regexId = /^[a-zA-Z][a-zA-Z0-9]{5,19}$/;
//         const regexPassword = /^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"'<>,.?/-]{5,11}$/;
//         const regexNickname = /^[a-zA-Z0-9가-힣]{2,12}$/;

//         if (!regexId.test(userData.id)) {
//             alert('아이디는 6~20자, 첫 자는 영어로 시작해야 합니다.');
//             return;
//         }

//         if (!regexPassword.test(userData.password)) {
//             alert('비밀번호는 6~12자, 첫 자는 영어로 시작해야 하며 특수문자도 가능합니다.');
//             return;
//         }

//         if (!regexNickname.test(userData.nickname)) {
//             alert('닉네임은 2~12자, 첫 자는 숫자가 아니어야 하며 한글과 영어만 가능합니다.');
//             return;
//         }

//         // 유효성 검사 통과 후 회원가입 요청
//         fetch(`/api/users/register`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ User: userData }),
//         }).then(response => response.json())
//           .then(data => {
//               if (data.status === 200) {
//                   alert(data.detail);
//               } else {
//                   alert(data.detail);
//               }
//           });
//     }

//     // 회원가입 - 기업
//     function registerManager(companyData) {
//         const regexId = /^[a-zA-Z][a-zA-Z0-9]{5,19}$/;
//         const regexPassword = /^[a-zA-Z][a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"'<>,.?/-]{5,11}$/;

//         if (!regexId.test(companyData.id)) {
//             alert('아이디는 6~20자, 첫 자는 영어로 시작해야 합니다.');
//             return;
//         }

//         if (!regexPassword.test(companyData.password)) {
//             alert('비밀번호는 6~12자, 첫 자는 영어로 시작해야 하며 특수문자도 가능합니다.');
//             return;
//         }

//         // 유효성 검사 통과 후 기업회원 가입 요청
//         fetch(`/api/company/register`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ Manager: companyData }),
//         }).then(response => response.json())
//           .then(data => {
//               if (data.status === 200) {
//                   alert(data.detail);
//               } else {
//                   alert(data.detail);
//               }
//           });
//     }
// });
