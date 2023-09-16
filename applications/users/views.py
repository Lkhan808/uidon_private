import requests
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from applications.users.managers import UserManager
from applications.users.models import User
from applications.users.serializers import SignUpSerializer, SignInSerializer, UserSerializer, PasswordResetSerializer, \
    ChangePassswordSerializer

from applications.users.services import UserService
from django.contrib.auth import authenticate
from applications.users.utils import generate_jwt_for_user
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
def sign_up_view(request: Request):
    if request.method == "POST":
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            UserService.send_mail_sign_up(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            return Response("Email send succesfully")


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
        if not user:
            error = status.HTTP_403_FORBIDDEN
            return Response(data={"user not found": error})

        if user.is_active:
            tokens = generate_jwt_for_user(user)
            return Response(data={"tokens": tokens, "user-data": UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Чел аккаунт не активный"}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def password_reset(request):
    try:
        email = request.data.get('email')
        try:
            UserService.send_mail_reset(email=email)
        except User.DoesNotExist:
            return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def password_reset_confirm(request: Request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data['new_password1']
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please submit a POST request to reset your password.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    user = request.user
    if request.method == 'PUT':
        serializer = ChangePassswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            new_password = serializer.validated_data['new_password']
            if check_password(password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Текущий пароль неверен.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def change_email_view(request):
    user = request.user
    if request.method == 'PATCH':
        new_email = request.data.get('new_email')
        if new_email and new_email != user.email:
            user.email = new_email
            user.save()
        else:
            return Response(data="new email is unreached or new email is similar with old email")
    return Response(data='email changed successfully', status=status.HTTP_200_OK)


@api_view(['GET'])
def google_login(request):
    password = make_password(UserManager().make_random_password())
    if request.method == 'GET':
        authorization_code = request.query_params.get('code')
        if not authorization_code:
            return Response(
                data={"message": "Authorization code is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Step 2: Exchange the authorization code for an access token and refresh token
        response = UserService.exchange_code_for_tokens(authorization_code=authorization_code)
        token_response = response.json()
        if 'error' in token_response:
            return Response(
                data={"message": token_response.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')

        # Step 3: Use the access token to fetch user information
        user_info = UserService.get_user_info_from_google(access_token=access_token)

        if 'error' in user_info:
            return Response(
                data={"message": user_info.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            user = User.objects.get(email=user_info["email"])
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=user_info["email"],
                password=password,
                role=request.data.get('role')
            )
            user.is_active = True
            user.save()
        jwt_tokens = generate_jwt_for_user(user)
        redirect_url = f'http://localhost:8003/?access_token={jwt_tokens["access"]}&refresh_token={jwt_tokens["refresh"]}'
        return HttpResponseRedirect(redirect_url)
