from rest_framework import serializers
from .models import Order, Ordering

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
