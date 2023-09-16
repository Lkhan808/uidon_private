from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra):
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_staff', True)
        extra.setdefault('is_active', True)
        extra.setdefault('role', 'customer')
        return self._create_user(email, password, **extra)

    def make_random_password(
            self,
            length=10,
            allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

