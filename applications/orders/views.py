from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderResponse, FavoriteOrder
from .serializers import OrderSerializer, OrderResponseSerializer
from applications.profiles.models import ExecutorProfile, CustomerProfile
from .decorators import require_executor
from .permissions import IsCustomerOrReadOnly, IsExecutorPermission


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Только аутентифицированные пользователи могут создавать заказы
def create_order(request):
    user = request.user

    # Проверяем, является ли пользователь заказчиком (customer)
    if hasattr(user, 'customer_profile'):
        # Если пользователь - заказчик, то он может создавать заказы
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            skill = serializer.validated_data.pop('skill')
            # Устанавливаем текущего пользователя как заказчика
            serializer.validated_data['customer'] = user.customer_profile
            order = Order(**serializer.validated_data)
            order.save()
            order.skill.set(skill)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Если пользователь не является заказчиком, возвращаем ошибку
        return Response({'error': 'Вы не являетесь заказчиком и не можете создавать заказы'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.filter(status='новый') # Фильтруем заказы по статусу "новый"
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_orders_list(request):
    # Получаем текущего аутентифицированного пользователя
    user = request.user

    # Проверяем, есть ли у пользователя профиль заказчика
    if not hasattr(user, 'customer_profile'):
        return Response({'error': 'Пользователь не является заказчиком'}, status=status.HTTP_403_FORBIDDEN)

    # Получаем заказы, созданные этим заказчиком
    customer_orders = Order.objects.filter(customer=user.customer_profile)
    serializer = OrderSerializer(customer_orders, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_close_orders_list(request):
    user = request.user

    if not hasattr(user, 'customer_profile'):
        return Response({'error': 'Пользователь не является заказчиком'}, status=status.HTTP_403_FORBIDDEN)

    customer_close_orders = Order.objects.filter(customer=user.customer_profile, status='закрыт')
    serializer = OrderSerializer(customer_close_orders, many=True)

    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsCustomerOrReadOnly])  # Применяем наши разрешения
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
@permission_classes([IsExecutorPermission])
def create_order_response(request):
    order_id = request.data.get('order_id')

    if not order_id:
        return Response({'message': 'Идентификатор заказа обязателен'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    # Получаем текущего исполнителя (предполагается, что вы авторизованы как исполнитель)
    executor = request.user.executor_profile

    # Создаем объект OrderResponse, автоматически устанавливая executor
    response = OrderResponse(order=order, executor=executor)
    response.save()

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
