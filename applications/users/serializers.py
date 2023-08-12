from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from applications.users import models
from applications.users.services import (
    UserService,
    ExecutorService,
    fetch_all,
    CustomerService
)

user_unique_validator = UniqueValidator(fetch_all(UserService.model))
executor_unique_validator = UniqueValidator(fetch_all(ExecutorService.model))
customer_unique_validator = UniqueValidator(fetch_all(CustomerService.model))


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[
        UserService.model.email_validator
    ])
    password = serializers.CharField(write_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[
        user_unique_validator,
        UserService.model.email_validator
    ])
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserService.model.ROLE_CHOICES)


class ExecutorListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profession = serializers.CharField()


class ExecutorRetrieveSerializer(ExecutorListSerializer):
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    education_level = serializers.CharField()
    biography = serializers.CharField()
    date_birth = serializers.DateField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    gender = serializers.CharField()
    location = serializers.CharField()
    phone = serializers.CharField()
    skills = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    educations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    languages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    portfolios = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contacts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    average_rating = serializers.FloatField()


class ExecutorValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutorProfile
        fields = "__all__"


class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    avatar = serializers.ImageField()
    first_name = serializers.CharField()
    location = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)


class CustomerValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerService.model
        fields = "__all__"
