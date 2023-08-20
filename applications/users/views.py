from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from applications.users.models import User
from applications.users.serializers import (
    SignUpSerializer, SignInSerializer, UserSerializer
)
from applications.users.serializers import SignUpSerializer, SignInSerializer, UserSerializer

from applications.users.services import send_email_verification, verify_email
from django.contrib.auth import authenticate
from applications.users.utils import generate_jwt_for_user
from rest_framework.decorators import api_view


@api_view(["POST"])
def sign_up_view(request: Request):
    if request.method == "POST":
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            send_email_verification(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def verify_email_view(request: Request, user_id, jwt):
    if request.method == "GET":
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'msg': 'Учетная запись успешно активирована'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"msg": "user not found"}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def sign_in_view(request: Request):
    if request.method == "POST":
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if user.is_active:
            tokens = generate_jwt_for_user(user)
            return Response(data={"tokens": tokens, "user-data": UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:            return Response(data={"Чел аккаунт не активный"}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
