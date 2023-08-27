from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from applications.profiles.models import ExecutorProfile, CustomerProfile
from applications.profiles.serializers import ExecutorSerializer, CustomerSerializer


@api_view(["GET", "POST"])
def executors_list_view(request: Request):
    """ Создание или список фрилансеров """
    if request.method == "GET":
        executors = ExecutorProfile.objects.all()
        serializer = ExecutorSerializer(executors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = ExecutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PUT"])
def executor_detail_view(request: Request, pk):
    """ Детальный просмотр, удаление, изменение фрилансера """
    executor = ExecutorProfile.objects.get(pk=pk)
    if request.method == "GET":
        serializer = ExecutorSerializer(executor)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = ExecutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        executor.delete()
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
