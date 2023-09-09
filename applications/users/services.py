import json

import requests

from applications.users import models
from applications.users.utils import generate_jwt_for_user, send_mail_for_user, send_mail_reset_password
from rest_framework.exceptions import NotFound
from django.db.models import Model


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
    def get_user_info_from_google(cls, token):
        payload = {"access_token": token}
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo", params=payload
        )
        return json.loads(user_info.text)
