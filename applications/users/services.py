from applications.users.models import User
from config.settings import base
from django.core.mail import send_mail
from applications.users.utils import generate_jwt_for_user
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


def send_email_verification(data):
    user = User.objects.create_user(**data)
    tokens = generate_jwt_for_user(user)
    user.save()
    subject = 'Подтвердите свой EMAIL'
    message = f'\n{base.BASE_URL}api/auth/verify-email/{user.id}/{tokens["access"]}'
    from_email = base.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def verify_email(user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        return user
    raise ValidationError("User is already active")
