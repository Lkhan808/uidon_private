from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from applications.users.constants import ROLE_CHOICES, GENDER_CHOICES, EDUCATION_CHOICES
from applications.users.models import Skill
from applications.users.services import UserService, ExecutorService, CustomerService
from applications.users.utils import profile_with_user_exists

executor_unique_validator = UniqueValidator(ExecutorService.fetch_all())
customer_unique_validator = UniqueValidator(CustomerService.fetch_all())


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(UserService.fetch_all())])
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)


class ExecutorListSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=False)
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class ExecutorRetrieveSerializer(ExecutorListSerializer):
    biography = serializers.CharField()
    date_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    profession = serializers.CharField()
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    education_level = serializers.ChoiceField(EDUCATION_CHOICES)
    location = serializers.CharField()
    phone = serializers.CharField(validators=[executor_unique_validator])
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    educations = serializers.StringRelatedField(many=True, read_only=True)
    languages = serializers.StringRelatedField(many=True, read_only=True)
    reviews = serializers.StringRelatedField(many=True, read_only=True)


class ExecutorValidateSerializer(ExecutorRetrieveSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserService.fetch_all(),
        validators=[executor_unique_validator]
    )

    def create(self, validated_data):
        executor = ExecutorService.create_profile(validated_data)
        return executor

    def update(self, instance, validated_data):
        executor = ExecutorService.update_profile(instance, validated_data)
        return executor


class CustomerSerializer(ExecutorListSerializer):
    pass


class CustomerValidateSerializer(ExecutorListSerializer):
    phone = serializers.CharField(validators=[customer_unique_validator])
    location = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserService.fetch_all(),
        validators=[profile_with_user_exists]
    )

    def create(self, validated_data):
        user = validated_data["user"]
        customer = CustomerService.create_profile(validated_data)
        return customer

    def update(self, instance, validated_data):
        customer = CustomerService.update_profile(instance, validated_data)
        return customer
