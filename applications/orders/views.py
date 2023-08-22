from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Order, OrderResponse
from .serializers import OrderSerializer, OrderResponseSerializer
from applications.profiles.models import ExecutorProfile
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
    order_response = OrderResponse.objects.get(order=order, executor=executor)
    order_response.attached = True
    order_response.save()
    return Response({'message': 'Исполнитель назначен на заказ'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def executor_orders_view(request):
    user = request.user
    executor_profile = ExecutorProfile.objects.get(user=user)  # Получаем профиль исполнителя по пользователю

    orders_assigned = OrderResponse.objects.filter(executor=executor_profile, attached=True)
    orders_completed = OrderResponse.objects.filter(executor=executor_profile, completed=True)

    assigned_serializer = OrderResponseSerializer(orders_assigned, many=True)
    completed_serializer = OrderResponseSerializer(orders_completed, many=True)

    return Response({
        'assigned_orders': assigned_serializer.data,
        'completed_orders': completed_serializer.data
    })

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def close_order_view(request, order_id):
    user = request.user
    try:
        executor_profile = user.executor_profile
    except ExecutorProfile.DoesNotExist:
        return Response({'message': 'Профиль исполнителя не найден'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(pk=order_id, executor=executor_profile, status='в работе')
        order.status = 'закрыт'
        order.save()

        order_response = OrderResponse.objects.get(order=order, executor=executor_profile)
        order_response.completed = True
        order_response.attached = False  # Убираем из assigned_orders
        order_response.save()


        return Response(data="Заказ закрыт", status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'message': 'Заказ не найден или не может быть закрыт'}, status=status.HTTP_400_BAD_REQUEST)
