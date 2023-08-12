from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomerProfile
from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    ExecutorValidateSerializer,
    ExecutorRetrieveSerializer,
    ExecutorListSerializer,
    CustomerSerializer,
    CustomerValidateSerializer
)
from .services import UserService, ExecutorService, fetch_all, CustomerService
from django.contrib.auth import authenticate
from .utils import generate_jwt_for_user
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.send_mail_sign_up(serializer.validated_data)
        return Response(
            data={"msg": "На вашу почту отправлено письмо на подтверждение аккаунта"},
            status=status.HTTP_200_OK
        )


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request: Request, *args, **kwargs):
        user_id = self.kwargs["user_id"]
        user = UserService.fetch_one(user_id)
        user.is_active = True
        user.save()
        return Response({'msg': 'Account activated successfully'}, status=status.HTTP_200_OK)


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if user:
            tokens = generate_jwt_for_user(user=user)
            return Response(data={"tokens": tokens, "data": serializer.data}, status=status.HTTP_200_OK)
        raise AuthenticationFailed()


class ExecutorViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        if self.action == "list":
            return ExecutorService.executors_list()
        elif self.action == "retrieve":
            return ExecutorService.executor_detail()
        return fetch_all(ExecutorService.model)

    def get_serializer_class(self):
        if self.action == "list":
            return ExecutorListSerializer
        elif self.action == "retrieve":
            return ExecutorRetrieveSerializer
        return ExecutorValidateSerializer


class CustomerViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CustomerSerializer
        return CustomerValidateSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return CustomerService.customers_list()
        return fetch_all(CustomerService.model)