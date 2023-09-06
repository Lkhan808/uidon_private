from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.settings import base
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def send_mail_for_user(user: User, jwt):
    subject = 'Подтвердите свой EMAIL'
    message = (f'Перейдите по ссылке для подтверждения своего аккаунта:'
               f'\n{base.BASE_URL}api/auth/verify-email/{user.id}/{jwt["access"]}/')
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


def send_mail_reset_password(user: User):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    reset_url = f"{base.BASE_URL}api/auth/password-reset/confirm/{uid}/{str(token)}/"
    subject = 'Reset your password'
    message = f"Please click the following link to reset your password:\n{reset_url}"
    from_email = base.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
