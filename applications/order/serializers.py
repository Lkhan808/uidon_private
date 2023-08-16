from rest_framework import serializers
from .models import Order, Ordering
from applications.users.models import ExecutorProfile

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordering
        fields = '__all__'

class OrderChooseExecutorSerializer(serializers.Serializer):
    executor_id = serializers.IntegerField()
    order_id = serializers.IntegerField()

class OrderResponseSerializer(serializers.Serializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    executor_id = serializers.PrimaryKeyRelatedField(queryset=ExecutorProfile.objects.all())

