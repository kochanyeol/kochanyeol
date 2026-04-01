from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError('must have user email')
        # 유저 객체 생성
        # normalize_email 이메일 정규화(@ 뒤에 도메인 소문자로 통일)
        # 위치인자, 키워드인자 필드받기
        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        # set_password는 장고 소스코드에서 들어온 password에서 해시화 해서 make_password로 반환
        # 이후 반환 됀 make_password는 salt를 적용해서 self.password에 반환
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email=self.normalize_email(email), password=password, *args, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to='users/profile_images', default='users/blank_profile_image.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email