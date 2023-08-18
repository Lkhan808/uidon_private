from applications.users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from applications.users.services import get_all_users


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SignInSerializer(UserSerializer):
    pass


class SignUpSerializer(UserSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(get_all_users())])
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)


class VerificationEmailSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(write_only=True, min_length=6, max_length=6)
