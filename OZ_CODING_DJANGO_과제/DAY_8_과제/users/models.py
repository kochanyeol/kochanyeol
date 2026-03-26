from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.db.models import EmailField, CharField, BooleanField


# class User(AbstractBaseUser, PermissionsMixin):
    # 이미 password와 last_login 필드가 구현되어 있어 이 이외에 필드를 정희해주면 된다.
    # 그렇기에 PermissionsMixin도 같이 상속받아서 필요한 권한과 추가 db 테이블 구조 필드를 커스텀해야한다.

# class User(AbstractUser):
    # 여기서는 AbstractUser가 이미 PermissionsMixin을 포함하고 있어서
    # 테이블 구조와 권한 전부 장고가 정의해둔것을 바로 사용할 수 있다.
    # 만약 추가 필드가 필요하다면 이미 PermissionsMixin을 포함하고 있어서 그냥 작성하기만 하면된다.

class UserManager(BaseUserManager):
# BaseUserManager는 장고 기능으로
    # self.normalize_email(email)         이메일 정규화(소문자 변환, 공백 제거)
    # self.normalize_username(username)   유저이름 정규화(소문자 변환, 공백 제거)
    # self.model(...)                     User 객체 생성(회원가입할 때 User 모델의 필드값을 담은 객체를 생성)
    # self.make_random_password()         랜덤 비밀번호 생성
    # self.get_by_natural_key(username)   username으로 유저 찾기

    def create_user(self, email, password=None, *args, **kwargs):
    # 일반 유저 생성
    # 회원가입할 때 호출
    # 키워드 인자만 주로 받기에 *args를 사용할 경우가 거의 없지만 요구사항과 확장상을 고려해 작성
        email = self.normalize_email(email)
        # 이메일을 정규화해주기
        user = self.model(email=email, *args ,**kwargs)
        # email은 위치 인자로 필수 입력
        # name 같은 필수 필드도 *args로 위치 인자로 받을 수 있음
        # is_active 같은 선택 필드는 **kwargs로 키워드 인자로 받음
        user.set_password(password)
        # set_password는 비밀번호를 해싱해서 저장하는 메서드이다.
        user.save()
        return user

    def create_superuser(self, email, password=None, *args, **kwargs):
    # 관리자 생성 메서드로 python manage.py createsuperuser 할 때 호출된다.
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        # 기본 권한 값을 지정해주기 위함.
        # 이미 **kwargs에 값이 있으면 덮어쓰지 않는다
        return self.create_user(email, password, *args, **kwargs)
        # create_user을 불러와서 이메엘,비밀번호, 그리고 권한관련 내용을 넘겨서 관리자 생성

class User(AbstractBaseUser, PermissionsMixin):
    name = CharField(max_length=100)
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    # accounts.User와 역참조 이름 충돌 방지
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_user_permissions',
        blank=True,
    )

    objects = UserManager()
    # User.object.all() 같은 쿼리를 날릴 때 우리가 만든 UserManager을 사용
    # 회원가입시에 함수를 호출하여 회원가입 진행
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    # 로그인할 때 어떤 필드로 아이디를 사용할지 지정 - default='username'

    @property
    def username(self):
        return self.name
    # 템플릿에서{{ user.username }}으로 접근하면 기존에는 메서드여서 호출이 안돼어서
    # FBV에서 직접 처리하였지만 @property를 사용하면 변수처럼 접근을 가능하게 만들어줘서
    # {{ user.username }}으로 접근해도 self.name으로 잘 반환해준다.