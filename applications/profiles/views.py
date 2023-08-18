from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from applications.profiles.serializers import ExecutorListSerializer, ExecutorCreateSerializer, \
    ExecutorRetrieveSerializer, ExecutorUpdateSerializer
from applications.profiles.services import get_all_executors, create_executor, get_executor


@extend_schema(request=ExecutorListSerializer, responses={200: ExecutorListSerializer})
@api_view(["GET"])
def get_executors_view(request: Request):
    if request.method == "GET":
        executors = get_all_executors()
        serializer = ExecutorListSerializer(executors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(request=ExecutorCreateSerializer, responses={201: ExecutorCreateSerializer})
@api_view(["POST"])
def create_executor_view(request: Request):
    if request.method == "POST":
        serializer = ExecutorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        executor = create_executor(serializer.validated_data)
        return Response(data=ExecutorListSerializer(executor).data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(request=ExecutorRetrieveSerializer, responses={200: ExecutorRetrieveSerializer})
@api_view(["GET"])
def get_executor_view(request: Request, pk: int):
    if request.method == "GET":
        executor = get_executor(pk=pk)
        serializer = ExecutorRetrieveSerializer(executor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(request=None, responses={204: None})
@api_view(["DELETE"])
def delete_executor_view(request: Request, pk: int):
    if request.method == "DELETE":
        executor = get_executor(pk=pk)
        executor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
