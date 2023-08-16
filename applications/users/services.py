from django.db.models import Model, Prefetch, QuerySet
from applications.users.models import User, ExecutorProfile, CustomerProfile
from applications.users.utils import send_mail_for_user, generate_jwt_for_user
from rest_framework.exceptions import NotFound


class BaseService:
    model: Model

    @classmethod
    def fetch_one(cls, pk: int):
        try:
            return cls.model.objects.get(pk=pk)
        except cls.model.DoesNotExist:
            raise NotFound()

    @classmethod
    def fetch_all(cls):
        return cls.model.objects.all()


class UserService(BaseService):
    model = User

    @classmethod
    def send_mail_sign_up(cls, validated_data):
        user = cls.model.objects.create_user(**validated_data)
        jwt = generate_jwt_for_user(user)
        send_mail_for_user(user, jwt)


class ExecutorService(BaseService):
    model = ExecutorProfile

    @classmethod
    def get_executors(cls) -> QuerySet[Model]:
        queryset = cls.fetch_all().prefetch_related("skills")
        return queryset.only("id", "avatar", "profession", "last_name", "first_name")

    @classmethod
    def get_executor(cls) -> QuerySet[Model]:
        prefetch_list = ["skills", "portfolios", "contacts",
                         "languages", "educations", "reviews", "ratings"]
        queryset = cls.fetch_all()
        return queryset.prefetch_related(*prefetch_list).select_related("user")


class CustomerService(BaseService):
    model = CustomerProfile
