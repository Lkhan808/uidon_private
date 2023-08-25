from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.forms import SetPasswordForm
from applications.users.models import User
from applications.users.serializers import SignUpSerializer, SignInSerializer, UserSerializer, PasswordResetSerializer

from applications.users.services import UserService
from django.contrib.auth import authenticate, login
from applications.users.utils import generate_jwt_for_user
from rest_framework.decorators import api_view


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
