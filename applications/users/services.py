from applications.users.models import User
from config.settings import base
from django.core.mail import send_mail
from applications.users.utils import generate_confirmation_code
from rest_framework.exceptions import ValidationError


def send_email_verification(data):
    user = User.objects.create_user(**data)
    user.confirmation_code = generate_confirmation_code()
    user.save()
    subject = 'Подтвердите свой EMAIL'
    message = (f'На почту отправлен 6-значный код:'
               f'\n{base.BASE_URL}api/auth/verify-email/')
    from_email = base.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def get_all_users():
    return User.objects.all()


def verify_email(confirmation_code):
    try:
        user = User.objects.get(confirmation_code=confirmation_code)
        if not user.is_active:
            user.is_active = True
            user.save()
            return user
        raise ValidationError("User is already active")
    except User.DoesNotExist:
        raise ValidationError("User not found")
