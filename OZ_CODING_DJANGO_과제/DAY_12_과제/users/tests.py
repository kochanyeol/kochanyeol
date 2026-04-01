from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        # 테스트할 때 공용으로 쓸 정보 세팅
        # create_user, create_superuser 테스트에서
        # 공용으로 쓸 이메일, 비밀번호
        self.email = 'admin@exmple.com'
        self.password = 'qwer1234'

    def test_user_manager_create_user(self):
        # create_user로 유저 생성
        user = User.objects.create_user(
            email = self.email,
            password = self.password,
            nickname = '테스트유저',
        )
        # 생성한 유저랑 db에 유저랑 맞는지 확인
        self.assertEqual(user.email, self.email)
        # 비밀번호 해쉬화 체크
        self.assertTrue(user.check_password(self.password))
        # 일반 유저이기에 둘다 False로 기본값 설정
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)


    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(
            email = 'super@test.com',
            password = self.password,
            nickname = '슈퍼유저'
        )
        # 슈퍼 유저이기에 둘다 True로 기본값 설정
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


# > python manage.py test users
# Found 2 test(s).
# Creating test database for alias 'default'...
# Got an error creating the test database: (1007, "Can't create database 'test_day12'; database exists")
# Type 'yes' if you would like to try deleting the test database 'test_day12', or 'no' to cancel: yes
# Destroying old test database for alias 'default'...
# System check identified no issues (0 silenced).
# ..
# ----------------------------------------------------------------------
# Ran 2 tests in 0.427s
#
# OK
# Destroying test database for alias 'default'...