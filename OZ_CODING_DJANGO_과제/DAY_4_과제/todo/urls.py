from django.urls import path
from .views import todo_list, todo_info, todo_create, todo_delete, todo_update

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:id>/', todo_info, name='todo_info'),
    path('create/', todo_create, name='todo_create'),
    path('<int:id>/update/', todo_update, name='todo_update'),
    path('<int:id>/delete/', todo_delete, name='todo_delete'),
]