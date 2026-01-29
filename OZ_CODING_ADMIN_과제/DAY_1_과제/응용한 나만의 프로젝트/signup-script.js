// 다크모드 토글
function toggleDarkMode() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    
    if (body.classList.contains('light-mode')) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// 페이지 로드시 저장된 테마 적용
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const themeIcon = document.getElementById('theme-icon');
    
    document.body.classList.remove('light-mode', 'dark-mode');
    document.body.classList.add(savedTheme + '-mode');
    
    if (savedTheme === 'dark') {
        themeIcon.textContent = '☀️';
    } else {
        themeIcon.textContent = '🌙';
    }
});

// 에러 메시지 표시 함수
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

// 에러 메시지 초기화
function clearError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

// 모든 에러 메시지 초기화
function clearAllErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => {
        error.textContent = '';
        error.style.display = 'none';
    });
}

// 실시간 유효성 검사
document.addEventListener('DOMContentLoaded', () => {
    // 아이디 입력 검사
    document.getElementById('userId').addEventListener('input', (e) => {
        const value = e.target.value.trim();
        const idRegex = /^[a-zA-Z0-9]{4,20}$/;
        
        if (value && !idRegex.test(value)) {
            showError('id-error', '아이디는 4-20자의 영문, 숫자만 사용 가능합니다.');
        } else {
            clearError('id-error');
        }
    });

    // 비밀번호 입력 검사
    document.getElementById('password').addEventListener('input', (e) => {
        const value = e.target.value;
        const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$/;
        
        if (value && !passwordRegex.test(value)) {
            showError('password-error', '비밀번호는 영문, 숫자, 특수문자를 포함한 8-30자여야 합니다.');
        } else {
            clearError('password-error');
        }
        
        // 비밀번호 확인란이 입력되어 있으면 일치 여부 확인
        const confirmValue = document.getElementById('passwordConfirm').value;
        if (confirmValue) {
            if (value !== confirmValue) {
                showError('password-confirm-error', '비밀번호가 일치하지 않습니다.');
            } else {
                clearError('password-confirm-error');
            }
        }
    });

    // 비밀번호 확인 입력 검사
    document.getElementById('passwordConfirm').addEventListener('input', (e) => {
        const password = document.getElementById('password').value;
        const confirmValue = e.target.value;
        
        if (confirmValue && password !== confirmValue) {
            showError('password-confirm-error', '비밀번호가 일치하지 않습니다.');
        } else {
            clearError('password-confirm-error');
        }
    });

    // 이름 입력 검사
    document.getElementById('name').addEventListener('input', (e) => {
        const value = e.target.value.trim();
        const nameRegex = /^[가-힣a-zA-Z]{2,20}$/;
        
        if (value && !nameRegex.test(value)) {
            showError('name-error', '이름은 2-20자의 한글 또는 영문만 사용 가능합니다.');
        } else {
            clearError('name-error');
        }
    });

    // 전화번호 입력 검사
    document.getElementById('phone').addEventListener('input', (e) => {
        const value = e.target.value.trim();
        const phoneRegex = /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/;
        
        if (value && !phoneRegex.test(value)) {
            showError('phone-error', '올바른 전화번호 형식이 아닙니다. (예: 010-0000-0000)');
        } else {
            clearError('phone-error');
        }
    });

    // 이메일 입력 검사
    document.getElementById('email').addEventListener('input', (e) => {
        const value = e.target.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (value && !emailRegex.test(value)) {
            showError('email-error', '올바른 이메일 형식이 아닙니다.');
        } else {
            clearError('email-error');
        }
    });
});

// 회원가입 처리
function handleSignup(event) {
    event.preventDefault();
    
    // 모든 에러 메시지 초기화
    clearAllErrors();
    
    const userId = document.getElementById('userId').value.trim();
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('passwordConfirm').value;
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const genderElements = document.getElementsByName('gender');
    let gender = '';
    for (let i = 0; i < genderElements.length; i++) {
        if (genderElements[i].checked) {
            gender = genderElements[i].value;
            break;
        }
    }
    const email = document.getElementById('email').value.trim();
    
    let isValid = true;
    
    // 아이디 유효성 검사 (4-20자, 영문+숫자)
    const idRegex = /^[a-zA-Z0-9]{4,20}$/;
    if (!idRegex.test(userId)) {
        showError('id-error', '아이디는 4-20자의 영문, 숫자만 사용 가능합니다.');
        isValid = false;
    }
    
    // 비밀번호 유효성 검사 (8-30자, 영문+숫자+특수문자 포함)
    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$/;
    if (!passwordRegex.test(password)) {
        showError('password-error', '비밀번호는 영문, 숫자, 특수문자를 포함한 8-30자여야 합니다.');
        isValid = false;
    }
    
    // 비밀번호 확인
    if (password !== passwordConfirm) {
        showError('password-confirm-error', '비밀번호가 일치하지 않습니다.');
        isValid = false;
    }
    
    // 이름 유효성 검사 (2-20자, 한글 또는 영문)
    const nameRegex = /^[가-힣a-zA-Z]{2,20}$/;
    if (!nameRegex.test(name)) {
        showError('name-error', '이름은 2-20자의 한글 또는 영문만 사용 가능합니다.');
        isValid = false;
    }
    
    // 전화번호 유효성 검사
    const phoneRegex = /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/;
    if (!phoneRegex.test(phone)) {
        showError('phone-error', '올바른 전화번호 형식이 아닙니다. (예: 010-0000-0000)');
        isValid = false;
    }
    
    // 성별 선택 확인
    if (!gender) {
        showError('gender-error', '성별을 선택해주세요.');
        isValid = false;
    }
    
    // 이메일 유효성 검사
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('email-error', '올바른 이메일 형식이 아닙니다.');
        isValid = false;
    }
    
    if (!isValid) {
        return false;
    }
    
    // 사용자 정보 저장
    const userInfo = {
        userId: userId,
        password: password,
        name: name,
        phone: phone,
        gender: gender,
        email: email
    };
    
    localStorage.setItem('userId', userId);
    localStorage.setItem('userPassword', password);
    localStorage.setItem('userName', name);
    localStorage.setItem('userPhone', phone);
    localStorage.setItem('userGender', gender);
    localStorage.setItem('userEmail', email);
    
    // 회원가입 내용 알림창
    const genderText = gender === 'male' ? '남성' : gender === 'female' ? '여성' : '기타';
    const message = `
=== 회원가입 정보 ===

아이디: ${userId}
이름: ${name}
전화번호: ${phone}
성별: ${genderText}
이메일: ${email}

회원가입이 완료되었습니다!
    `;
    
    alert(message);
    
    // 회원가입 완료 페이지로 이동
    window.location.href = 'signup-complete.html';
    
    return false;
}