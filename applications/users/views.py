from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from applications.users.serializers import (
    SignUpSerializer, SignInSerializer,
    VerificationEmailSerializer, UserSerializer
)
from applications.users.services import send_email_verification, verify_email
from django.contrib.auth import authenticate
from applications.users.utils import generate_jwt_for_user
from rest_framework.decorators import api_view
from drf_spectacular.views import extend_schema


@extend_schema(request=SignUpSerializer, responses={201: SignUpSerializer})
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
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(request=VerificationEmailSerializer, responses={200: VerificationEmailSerializer})
@api_view(["POST"])
def verify_email_view(request: Request):
    if request.method == "POST":
        serializer = VerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = verify_email(serializer.data.get("confirmation_code"))
        return Response(data={"data": UserSerializer(user).data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(request=SignInSerializer, responses={200: SignInSerializer})
@api_view(["POST"])
def sign_in_view(request: Request):
    if request.method == "POST":
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if user.is_active:
            tokens = generate_jwt_for_user(user)
            return Response(data={"tokens": tokens, "user-data": UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Чел аккаунт не активный"}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
