from django.db import models
from django.conf import settings

# 모델은 db테이블 구조를 정의하고 db와 직접 소통하는 역할
# 뷰가 명령하면 모델은 db에서 꺼내와서 뷰에게 반환해준다.
# models.Model를 상속받는 순간부터 뷰에서 장고의 내장기능인 orm을 쓸 수 있다.
# 추가로 db생성, crud를 자동으로 처리해준다.

class Todo(models.Model):
    # settings.AUTH_USER_MODEL: 직접 User 모델을 import 하는 대신 설정값으로 참조
    # AUTH_USER_MODEL이 바뀌어도 이 코드는 수정 안 해도 됨
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title