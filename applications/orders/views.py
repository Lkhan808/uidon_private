from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Order, OrderResponse, FavoriteOrder
from .serializers import OrderSerializer, OrderResponseSerializer
from applications.profiles.models import ExecutorProfile
from .decorators import require_executor
from ..profiles.serializers import ExecutorSerializer


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

@api_view(['GET', 'PATCH', 'DELETE'])
def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response({'message': 'Заказ успешно удален'}, status=status.HTTP_204_NO_CONTENT)

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
    order.response_count += 1
    order.save()

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
    executor_profile = ExecutorProfile.objects.get(user=user)

    orders_assigned = OrderResponse.objects.filter(executor=executor_profile, attached=True)
    orders_completed = OrderResponse.objects.filter(executor=executor_profile, completed=True)

    assigned_orders_data = []
    for order_response in orders_assigned:
        assigned_order_data = OrderSerializer(order_response.order).data
        assigned_orders_data.append(assigned_order_data)

    completed_orders_data = []
    for order_response in orders_completed:
        completed_order_data = OrderSerializer(order_response.order).data
        completed_orders_data.append(completed_order_data)

    return Response({
        'assigned_orders': assigned_orders_data,
        'completed_orders': completed_orders_data
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_favorite(request, order_id):
    user = request.user
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    favorite, created = FavoriteOrder.objects.get_or_create(executor=user.executor_profile, order=order)
    if created:
        return Response({'message': 'Заказ успешно добавлен в избранное'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Заказ уже находится в избранном'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_favorite(request, order_id):
    user = request.user
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    try:
        favorite = FavoriteOrder.objects.get(executor=user.executor_profile, order=order)
        favorite.delete()
        return Response({'message': 'Заказ успешно удален из избранного'}, status=status.HTTP_204_NO_CONTENT)
    except FavoriteOrder.DoesNotExist:
        return Response({'message': 'Заказ не находится в избранном'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def favorite_orders_list(request):
    user = request.user
    favorite_orders = FavoriteOrder.objects.filter(executor=user.executor_profile)
    favorite_order_ids = favorite_orders.values_list('order_id', flat=True)

    orders = Order.objects.filter(id__in=favorite_order_ids)
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)
