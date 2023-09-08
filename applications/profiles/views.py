from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from applications.profiles.models import ExecutorProfile, CustomerProfile, ProfileView
from applications.profiles.serializers import ExecutorSerializer, CustomerSerializer, ExecutorProfileSerializer, CustomerProfileSerializer
from .permissions import IsCustomerPermission, IsExecutorPermission


@api_view(["GET"])
def executor_list_view(request):
    """ Список фрилансеров """
    executors = ExecutorProfile.objects.all()
    serializer = ExecutorSerializer(executors, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def executor_detail_view(request: Request, pk):
    """ Детальный просмотр фрилансера """
    executor_profile = ExecutorProfile.objects.get(pk=pk)
    current_user = request.user
    # Получить профиль пользователя, который просматривается
    profile_user = executor_profile.user

    if current_user.role == 'customer':
        # Проверить, является ли текущий пользователь автором профиля
        is_owner = current_user == profile_user

        # Проверить, был ли профиль уже просмотрен текущим пользователем
        if not is_owner and not ProfileView.objects.filter(viewer=current_user, profile=executor_profile).exists():
            executor_profile.view_count += 1
            executor_profile.save()
            ProfileView.objects.create(viewer=current_user, profile=executor_profile)

    serializer = ExecutorProfileSerializer(executor_profile)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def executor_create_view(request):
    user_id = request.user.id

    data = request.data.copy()
    data['user'] = user_id

    serializer = ExecutorSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE", "PATCH"])
@permission_classes([IsExecutorPermission])
def executor_path_delete_view(request: Request, pk):
    """ Удаление и частичное изменение фрилансера """
    executor_profile = ExecutorProfile.objects.get(pk=pk)

    if request.method == "PATCH":
        serializer = ExecutorSerializer(executor_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        executor_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def customer_list_view(request):
    customers = CustomerProfile.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def customers_detail_view(request: Request, pk):
    customer = CustomerProfile.objects.get(pk=pk)
    serializer = CustomerSerializer(customer)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def customer_create_view(request):
    user_id = request.user.id

    data = request.data.copy()
    data['user'] = user_id

    serializer = CustomerSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE", "PUT"])
@permission_classes([IsCustomerPermission])
def customer_path_delete_view(request: Request, pk):
    customer = CustomerProfile.objects.get(pk=pk)

    if request.method == "PUT":
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_profile_view(request):
    user = request.user  # Получаем текущего пользователя

    # Проверяем, является ли пользователь заказчиком (customer)
    if hasattr(user, 'customer_profile'):
        profile = user.customer_profile  # Получаем профиль заказчика
        serializer = CustomerProfileSerializer(profile)
    # Проверяем, является ли пользователь исполнителем (executor)
    elif hasattr(user, 'executor_profile'):
        profile = user.executor_profile  # Получаем профиль исполнителя
        serializer = ExecutorProfileSerializer(profile)
    else:
        return Response({"message": "Профиль не найден"}, status=400)

    return Response(serializer.data, status=200)

