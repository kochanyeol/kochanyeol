from django.contrib.auth.models import AbstractUser
from django.db import models

# AbstractUser: 장고 기본 User 모델(username, password, email 등)을 그대로 상속받는 클래스
# 커스텀 User 모델을 만들면 나중에 필드(ex. 프로필 사진, 전화번호 등)를 자유롭게 추가할 수 있다.
# 장고 공식 권장 방식: 프로젝트 시작 시 커스텀 User 모델을 만들어두는 것
class User(AbstractUser):
    pass
