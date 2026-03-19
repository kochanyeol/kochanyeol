from django.urls import path
from member import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login, name='login'),
]