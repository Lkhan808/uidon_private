import requests
from applications.users import models
from applications.users.utils import generate_jwt_for_user, send_mail_for_user, send_mail_reset_password
from rest_framework.exceptions import NotFound
from django.db.models import Model
from decouple import config as env

class BaseService:
    model: Model

    @classmethod
    def fetch_one(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except cls.model.DoesNotExist:
            raise NotFound


class UserService(BaseService):
    model = models.User

    @classmethod
    def send_mail_sign_up(cls, validated_data):
        user = cls.model.objects.create_user(**validated_data)
        jwt = generate_jwt_for_user(user)
        send_mail_for_user(user, jwt)

    @classmethod
    def send_mail_reset(cls, email):
        user = cls.model.objects.get(email=email)
        send_mail_reset_password(user=user)

    @classmethod
    def get_user_info_from_google(cls, access_token):
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        return user_info_response.json()

    @classmethod
    def exchange_code_for_tokens(cls, authorization_code):
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': authorization_code,
            'client_id': env('GOOGLE_CLIENT_ID'),
            'client_secret': env('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': env('GOOGLE_REDIRECT_URI'),
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=token_data)
        return response
