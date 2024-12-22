document.getElementById('phone-type').addEventListener('change', function() {
    const phoneType = this.value;

    // 요소 선택
    const mobilePhone = document.querySelector('.mobile-phone');
    const landlinePhone = document.querySelector('.landline-phone');
    
    // 필드 선택
    const mobileFields = document.querySelectorAll('.mobile-prefix, .mobile-middle, .mobile-last');
    const landlineFields = document.querySelectorAll('.landline-prefix, .landline-middle, .landline-last');

    if (phoneType === 'mobile') {
        // 휴대전화 필드에 대해 필수 속성 설정
        mobileFields.forEach(field => field.setAttribute('required', 'true'));
        landlineFields.forEach(field => field.removeAttribute('required'));

        // 휴대전화 보이기, 일반전화 숨기기
        mobilePhone.style.display = 'flex';
        landlinePhone.style.display = 'none';

        // 휴대전화 필드에 포커스를 설정 (각각 개별적으로 focus 호출)
        if (mobileFields[0]) mobileFields[0].focus();

    } else if (phoneType === 'landline') {
        // 일반전화 필드에 대해 필수 속성 설정
        landlineFields.forEach(field => field.setAttribute('required', 'true'));
        mobileFields.forEach(field => field.removeAttribute('required'));

        // 일반전화 보이기, 휴대전화 숨기기
        mobilePhone.style.display = 'none';
        landlinePhone.style.display = 'flex';

        // 일반전화 필드에 포커스를 설정
        if (landlineFields[0]) landlineFields[0].focus();
    } else {
        // '선택' 상태일 때는 모든 필드를 숨기고 필수 속성을 제거
        mobileFields.forEach(field => field.removeAttribute('required'));
        landlineFields.forEach(field => field.removeAttribute('required'));

        mobilePhone.style.display = 'none';
        landlinePhone.style.display = 'none';
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); 

    // 폼 제출 이벤트 리스너 추가
    form.addEventListener('submit', function(event) {
        // 폼 유효성 검사
        if (form.checkValidity()) {
            alert("저장되었습니다.");
            window.location.href = '../../index.html';
        } else {
            event.preventDefault(); 
            form.reportValidity(); 
        }
    });
});