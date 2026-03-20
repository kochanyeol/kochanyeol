from django.urls import path
from .cb_views import (
TodoListView,
TodoCreateView,
TodoDeleteView,
TodoDetailView,
TodoUpdateView,
)

# 사용자에게 요청이 오면 url과 매핑해주는 역할
# 그리고 어떤 view로 보내줄지 결정해준다
# fastapi에서는 라우터에서 데코를 붙여 url과 함수를 묶어서 표현했지만
# django에서는 이 둘을 나눠서 관리한다.
# urls는 MTV(모델,템플릿,뷰)패턴 밖에서 라우팅만 담당한다.

urlpatterns = [
    path('todo/', TodoListView.as_view(), name='cbv_todo_list'),
    path('todo/create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_detail')
]