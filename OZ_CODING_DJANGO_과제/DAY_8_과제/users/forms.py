from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
    # model, fields, widgets 등등 설정을 위해 Meta 클래스 생성
    # UserCreationForm은 장고에 내장되어있는 중복체크, 유효성 검사 등등을 위해 상속받아서 사용
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # password1, password2는 Meta.widgets로 적용이 안 돼서 직접 오버라이드
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )