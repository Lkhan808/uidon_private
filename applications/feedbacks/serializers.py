from rest_framework import serializers
from .models import FeedbackOnExecutor, FeedbackOnCustomer

class FeedbackOnExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackOnExecutor
        fields = "__all__"


class FeedbackOnCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackOnCustomer
        fields = "__all__"