from django.db.models import Model, Prefetch
from applications.users import models
from applications.users.models import CustomerProfile
from applications.users.utils import send_mail_for_user, generate_jwt_for_user
from rest_framework.exceptions import NotFound


def fetch_all(model):
    return model.objects.all()


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


class ExecutorService(BaseService):
    model = models.ExecutorProfile

    @classmethod
    def executors_list(cls):
        queryset = fetch_all(cls.model).only(
            "id", "avatar", "profession", "last_name", "first_name"
        )
        return queryset

    @classmethod
    def executor_detail(cls):
        prefetch_list = [
            Prefetch("skills", queryset=fetch_all(models.Skill)),
            Prefetch("portfolios", queryset=fetch_all(models.Portfolio)),
            Prefetch("contacts", queryset=fetch_all(models.Contact)),
            Prefetch("languages", queryset=fetch_all(models.Language)),
            Prefetch("educations", queryset=fetch_all(models.Education)),
            Prefetch("reviews", queryset=fetch_all(models.Review)),
        ]
        queryset = (fetch_all(cls.model)
                    .prefetch_related(*prefetch_list)
                    .select_related("user")
                    )
        return queryset


class CustomerService(BaseService):
    model = CustomerProfile

    @classmethod
    def customers_list(cls):
        queryset = fetch_all(cls.model).select_related("user")
        return queryset
