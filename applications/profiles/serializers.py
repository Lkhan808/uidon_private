from rest_framework import serializers
from applications.profiles.models import ExecutorProfile, CustomerProfile
from applications.qualifications.serializers import ContactSerializer, LanguageSerializer, PortfolioSerializer, \
    SkillSerializer


class ExecutorSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)
    portfolios = PortfolioSerializer(many=True, required=False)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = ExecutorProfile
        fields = "__all__"

class ExecutorListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)
    class Meta:
        model = ExecutorProfile
        fields = ["id", "full_name", "avatar", "location", "biography", "profession", "salary_method", "salary", "skills", "average_rating"]


    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ExecutorProfileSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)
    portfolios = PortfolioSerializer(many=True, required=False)
    feedback_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)

    class Meta:
        model = ExecutorProfile
        fields = '__all__'

    def get_feedback_count(self, obj):
        return obj.get_feedback_count()

    def get_average_rating(self, obj):
        return obj.get_average_rating()



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"

class CustomerProfileSerializer(serializers.ModelSerializer):
    feedback_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def get_feedback_count(self, obj):
        return obj.get_feedback_count()

    def get_average_rating(self, obj):
        return obj.get_average_rating()