from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.conf import settings


def send_verification_email(user, request):
    signer = TimestampSigner()
    token = signer.sign(user.email)
    # signing으로 유저 id를 암호화해서 토큰 생성

    verification_url = f"http://{request.get_host()}/users/verify/?code={token}"
    # 인증 링크 생성

    send_mail(
        subject='이메일 인증',
        message=f'아래 링크를 클릭하여 이메일을 인증해주세요.\n{verification_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
