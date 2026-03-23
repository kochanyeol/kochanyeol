from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse

User = get_user_model()

# 5일차에서는 딱히 오류가 없어서 찾지 못했지만 6일차에서 다시 해보니 오류가 발생하여 수정
# 회원가입 폼을 장고 기본 기능을 사용하여 장고 기본 User을 써서 models.py에 정의한 User을 찾지 못함.
# 그래서 뷰에서 장고 기본 기능 UserCreationForm에 Meta를 사용해서 models.py에 정의한 모델을 교체
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect(reverse('cbv_todo_list'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect(reverse('login'))

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})