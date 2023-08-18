from rest_framework import serializers
from .models import Order, OrderResponse

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderResponse
        fields = '__all__'
