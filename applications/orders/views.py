from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderResponse
from .serializers import OrderSerializer, OrderResponseSerializer
from ..users.models import ExecutorProfile
from .decorators import require_executor

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        skill = serializer.validated_data.pop('skill')
        order = Order.objects.create(**serializer.validated_data)
        order.skill.set(skill)
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['POST'])
@require_executor
def create_order_response(request):
    order_id = request.data.get('order_id')
    executor_id = request.data.get('executor_id')

    if not order_id or not executor_id:
        return Response({'message': 'Идентификатор заказа и исполнителя обязательны'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(pk=order_id)
        executor = ExecutorProfile.objects.get(pk=executor_id)
    except (Order.DoesNotExist, ExecutorProfile.DoesNotExist):
        return Response({'message': 'Заказ или исполнитель не найдены'}, status=status.HTTP_404_NOT_FOUND)

    response = OrderResponse.objects.create(order=order, executor=executor)
    return Response({'message': 'Отклик успешно создан'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_responses_for_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    responses = order.orderings.all()
    serializer = OrderResponseSerializer(responses, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def assign_executor_to_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    executor_id = request.data.get('executor_id')
    if not executor_id:
        return Response({'error': 'Не указан ID исполнителя'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        executor = ExecutorProfile.objects.get(id=executor_id)
    except ExecutorProfile.DoesNotExist:
        return Response({'error': 'Исполнитель с указанным ID не найден'}, status=status.HTTP_404_NOT_FOUND)

    order.executor = executor
    order.status = 'в работе'
    order.save()
    return Response({'message': 'Исполнитель назначен на заказ'})


@api_view(['POST'])
def leave_order_review(request, order_response_id):
    response = OrderResponse.objects.get(pk=order_response_id)
    review_text = request.data.get('review_text')
    # Создайте модель отзыва и свяжите его с заказом, исполнителем и текстом отзыва
    # order_review = OrderReview.objects.create(order=response.order, executor=response.executor, review_text=review_text)
    return Response({'message': 'Отзыв успешно оставлен'}, status=status.HTTP_201_CREATED)
