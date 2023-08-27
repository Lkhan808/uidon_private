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
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if new_password1 and new_password2 and new_password1 == new_password2:
            return data
        else:
            raise serializers.ValidationError("Passwords do not match.")


class ChangePassswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=3, required=True)

    def validate(self, data):
        password = data.get('password')
        new_password = data.get('new_password')

        if password and new_password and new_password != password:
            return data
        else:
            raise serializers.ValidationError("Passwords shouldn't match.")
