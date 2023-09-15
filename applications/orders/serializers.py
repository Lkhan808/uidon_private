from rest_framework import serializers
from .models import Order, OrderResponse, FavoriteOrder
from applications.profiles.serializers import ExecutorCRUDSerializer
from applications.qualifications.serializers import SkillSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    class Meta:
        model = Order
        exclude = ['executor']

class OrderResponseSerializer(serializers.ModelSerializer):
    executor = ExecutorCRUDSerializer()
    class Meta:
        model = OrderResponse
        fields = '__all__'


class FavoriteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteOrder
        fields = '__all__'