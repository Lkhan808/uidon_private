from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from applications.profiles.models import ExecutorProfile, CustomerProfile, ProfileView
from applications.profiles.serializers import ExecutorSerializer, CustomerSerializer, ExecutorProfileSerializer
from django.contrib.sessions.models import Session


@api_view(["GET", "POST"])
def executors_list_view(request: Request):
    """ Создание или список фрилансеров """
    if request.method == "GET":
        search_param = request.query_params.get('search', '')
        skill_param = request.query_params.get('skills', '')  # Получить параметр запроса "skills"
        salary_type_param = request.query_params.get('salary_type', '')  # Получить параметр запроса "salary_type"
        executors = ExecutorProfile.objects.filter(
            Q(profession__icontains=search_param),
            Q(profession__icontains=skill_param),
            Q(profession__icontains=salary_type_param))
        serializer = ExecutorSerializer(executors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = ExecutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PATCH"])  # Заменяем "PUT" на "PATCH" здесь
def executor_detail_view(request: Request, pk):
    """ Детальный просмотр, удаление, частичное изменение фрилансера """
    executor_profile = ExecutorProfile.objects.get(pk=pk)
    current_user = request.user
    # Получить профиль пользователя, который просматривается
    profile_user = executor_profile.user
    if request.method == 'GET':
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
    elif request.method == "PATCH":  # Изменяем условие на "PATCH" здесь
        serializer = ExecutorSerializer(executor_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        executor_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def customers_list_view(request: Request):
    """ Создание или список заказчиков """
    if request.method == "GET":
        customers = CustomerProfile.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PUT"])
def customer_detail_view(request: Request, pk):
    """ Детальный просмотр, удаление, изменение фрилансера """
    customer = CustomerProfile.objects.get(pk=pk)
    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
