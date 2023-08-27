from rest_framework import serializers
from applications.profiles.models import ExecutorProfile, CustomerProfile




class ExecutorSerializer(serializers.ModelSerializer):
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    languages = serializers.StringRelatedField(many=True, read_only=True)
    portfolios = serializers.StringRelatedField(many=True, read_only=True)
    feedbacks_on_executor = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ExecutorProfile
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['skills'] = [skill.name for skill in instance.skills.all()]
        return data


class CustomerSerializer(serializers.ModelSerializer):
    feedbacks_on_customer = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = CustomerProfile
        fields = "__all__"

    def get_ratings(self, obj):
        feedbacks = obj.feedbacks_on_executor.all()
        return [feedback.rating for feedback in feedbacks]

    def get_descriptions(self, obj):
        feedbacks = obj.feedbacks_on_executor.all()
        return [feedback.description for feedback in feedbacks]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ratings'] = self.get_ratings(instance)
        data['descriptions'] = self.get_descriptions(instance)
        return data