// 다크모드 토글
function toggleDarkMode() {
    const body = document.body;
    if (body.classList.contains('light-mode')) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
    }
}

// 페이지 로드시 저장된 테마 적용
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.remove('light-mode', 'dark-mode');
    document.body.classList.add(savedTheme + '-mode');

    // 로그인 상태 확인
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const showLoginButton = localStorage.getItem('showLoginButton') === 'true';
    
    // 회원가입 완료 후라면 로그인 버튼 표시
    if (showLoginButton && !isLoggedIn) {
        updateAuthButtons(false, true);
        localStorage.removeItem('showLoginButton');
    } else {
        updateAuthButtons(isLoggedIn, false);
    }
});

// 드롭다운 토글
function toggleDropdown() {
    document.getElementById('categoryDropdown').classList.toggle('show');
}

// 카테고리 선택
function selectCategory(category) {
    document.querySelector('.dropdown-button').textContent = category;
    document.getElementById('categoryDropdown').classList.remove('show');
}

// 외부 클릭시 드롭다운 닫기
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
        const dropdowns = document.getElementsByClassName('dropdown-content');
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].classList.remove('show');
        }
    }
    
    // 모달 외부 클릭시 닫기
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// 페이지 변경
let currentPage = 1;
function changePage(page) {
    const buttons = document.querySelectorAll('.pagination button');
    
    if (page === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (page === 'next' && currentPage < 3) {
        currentPage++;
    } else if (typeof page === 'number') {
        currentPage = page;
    }

    buttons.forEach(btn => btn.classList.remove('active'));
    buttons[currentPage].classList.add('active');
}

// 모달 관련 함수
function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 로그인 처리
function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const savedEmail = localStorage.getItem('userEmail');
    const savedPassword = localStorage.getItem('userPassword');

    if (email === savedEmail && password === savedPassword) {
        localStorage.setItem('isLoggedIn', 'true');
        
        // 폼 초기화
        document.getElementById('login-email').value = '';
        document.getElementById('login-password').value = '';
        
        alert('로그인 성공!');
        closeModal('loginModal');
        updateAuthButtons(true);
    } else {
        alert('이메일 또는 비밀번호가 일치하지 않습니다.');
    }
    
    return false;
}

// 로그인 처리
function handleLogin(event) {
    event.preventDefault();
    const userId = document.getElementById('login-id').value.trim();
    const password = document.getElementById('login-password').value;

    const savedUserId = localStorage.getItem('userId');
    const savedPassword = localStorage.getItem('userPassword');

    if (userId === savedUserId && password === savedPassword) {
        localStorage.setItem('isLoggedIn', 'true');
        
        // 폼 초기화
        document.getElementById('login-id').value = '';
        document.getElementById('login-password').value = '';
        
        alert('로그인 성공!');
        closeModal('loginModal');
        updateAuthButtons(true);
    } else {
        alert('아이디 또는 비밀번호가 일치하지 않습니다.');
    }
    
    return false;
}

// 로그아웃 처리
function logout() {
    localStorage.setItem('isLoggedIn', 'false');
    alert('로그아웃 되었습니다.');
    updateAuthButtons(false);
}

// 인증 버튼 상태 업데이트
function updateAuthButtons(isLoggedIn, showLogin = false) {
    const authButton = document.getElementById('authButton');
    const loginButton = document.getElementById('loginButton');
    const logoutButton = document.getElementById('logoutButton');

    if (isLoggedIn) {
        // 로그인된 상태: 로그아웃 버튼만 표시
        authButton.style.display = 'none';
        loginButton.style.display = 'none';
        logoutButton.style.display = 'block';
    } else if (showLogin) {
        // 회원가입 완료 후: 로그인 버튼만 표시
        authButton.style.display = 'none';
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
    } else {
        // 기본 상태: 회원가입 버튼만 표시
        authButton.style.display = 'block';
        loginButton.style.display = 'none';
        logoutButton.style.display = 'none';
    }
}