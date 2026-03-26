from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.shortcuts import render, redirect
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

from utils.email import send_verification_email
from .forms import SignupForm, LoginForm
from .models import User

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        send_verification_email(user, self.request)
        return render(self.request, 'registration/signup_done.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse_lazy('cbv_todo_list'))

def verify_email(request):
    code = request.GET.get('code')
    signer = TimestampSigner()
    try:
        email = signer.unsign(code, max_age=1800)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return render(request, 'registration/verify_success.html')
    except (SignatureExpired, BadSignature, User.DoesNotExist):
        return render(request, 'registration/verify_failed.html')
