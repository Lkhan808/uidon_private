from django.core.mail import send_mail
from config.settings import base
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def send_mail_for_user(user: User, jwt):
    subject = 'Подтвердите свой EMAIL'
    message = (f'Перейдите по ссылке для подтверждения своего аккаунта:'
               f'\n{base.BASE_URL}api/verify-email/{user.id}/{jwt["access"]}/')
    from_email = base.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def generate_jwt_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {
        "access": str(access),
        "refresh": str(refresh)
    }
