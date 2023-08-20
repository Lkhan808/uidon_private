from applications.users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SignInSerializer(UserSerializer):
    pass


class SignUpSerializer(UserSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())])
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)


class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)