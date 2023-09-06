from rest_framework import serializers
from .models import Order, OrderResponse, FavoriteOrder
from ..profiles.serializers import ExecutorSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderResponseSerializer(serializers.ModelSerializer):
    executor = ExecutorSerializer()
    class Meta:
        model = OrderResponse
        fields = '__all__'


class FavoriteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteOrder
        fields = '__all__'