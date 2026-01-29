function toggleDarkMode() {
  document.body.classList.toggle("dark");
}

document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const userId = document.getElementById("userId").value.trim();
  const password = document.getElementById("password").value;
  const passwordCheck = document.getElementById("passwordCheck").value;
  const name = document.getElementById("name").value.trim();
  const gender = document.getElementById("gender").value;
  const phone = document.getElementById("phone").value.trim();
  const email = document.getElementById("email").value.trim();

  const pwRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,30}$/;
// 새로운 비교연산자 표기법 이번기회에 배웠습니다.
  if (!userId || !password || !passwordCheck || !name || !gender || !phone || !email) {
    alert("모든 항목을 입력해주세요.");
    return;
  }

  if (!pwRegex.test(password)) {
    alert("비밀번호는 영문, 숫자, 특수문자를 포함한 8자 이상 30자 미만이어야 합니다.");
    return;
  }

  if (password !== passwordCheck) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  alert(
    `회원가입이 완료되었습니다.\n\n` +
    `아이디: ${userId}\n` +
    `이름: ${name}\n` +
    `성별: ${gender}\n` +
    `전화번호: ${phone}\n` +
    `이메일: ${email}`
  );
// 다시 원래 페이지로 돌아기게 만들기, 참고 WINDOW는 내장되어있기에 생략가능
  window.location.href = "admin.html";
});

