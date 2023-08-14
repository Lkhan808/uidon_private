from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed, NotFound
from applications.users.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ExecutorListSerializer,
    ExecutorRetrieveSerializer,
    ExecutorValidateSerializer,
    CustomerSerializer,
    CustomerValidateSerializer
)
from applications.users.services import UserService, ExecutorService, CustomerService
from django.contrib.auth import authenticate
from applications.users.utils import generate_jwt_for_user
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from applications.users.permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter


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

        try:
            user = UserService.fetch_one(user_id)
        except NotFound:
            return Response({'msg': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()
        return Response({'msg': 'Учетная запись успешно активирована'}, status=status.HTTP_200_OK)


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is not None:
            tokens = generate_jwt_for_user(user=user)
            return Response(data={"tokens": tokens, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Неверные учетные данные. Пожалуйста, проверьте логин и пароль.")


class ExecutorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['average_rating']

    def get_queryset(self):
        if self.action == "list":
            return ExecutorService.get_executors()
        elif self.action == "retrieve":
            return ExecutorService.get_executor()
        return ExecutorService.fetch_all()

    def get_serializer_class(self):
        if self.action == "list":
            return ExecutorListSerializer
        elif self.action == "retrieve":
            return ExecutorRetrieveSerializer
        return ExecutorValidateSerializer


class CustomerViewSet(ModelViewSet):
    queryset = CustomerService.fetch_all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['average_rating']

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CustomerSerializer
        return CustomerValidateSerializer
