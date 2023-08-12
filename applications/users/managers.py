from django.contrib.auth.models import BaseUserManager


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
