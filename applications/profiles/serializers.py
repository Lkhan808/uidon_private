from rest_framework import serializers
from applications.profiles.models import ExecutorProfile
from applications.profiles.services import get_all_executors
from applications.qualifications.services import get_all_skills
from applications.users.services import get_all_users
from rest_framework.validators import UniqueValidator


class AbstractExecutorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profession = serializers.CharField()
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    biography = serializers.CharField()
    phone = serializers.CharField()
    location = serializers.CharField()
    skills = serializers.StringRelatedField(many=True, read_only=True)


class ExecutorListSerializer(AbstractExecutorSerializer):
    pass


class ExecutorCreateSerializer(AbstractExecutorSerializer):
    date_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=ExecutorProfile.GENDER_CHOICES)
    education_level = serializers.ChoiceField(choices=ExecutorProfile.EDUCATION_CHOICES)
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=get_all_skills())
    user = serializers.PrimaryKeyRelatedField(queryset=get_all_users(),
                                              validators=[UniqueValidator(get_all_executors())])


class ExecutorRetrieveSerializer(AbstractExecutorSerializer):
    date_birth = serializers.DateField()
    gender = serializers.CharField()
    education_level = serializers.CharField()


class ExecutorUpdateSerializer(ExecutorCreateSerializer):
    user = None
