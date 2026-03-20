from django.shortcuts import render

from django.conf import settings # settings에서 가져오면 추후 이름이 변경되면 찾기 어려움
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.urls import reverse




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
    django_logout(request)
    return redirect(reverse('login'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})