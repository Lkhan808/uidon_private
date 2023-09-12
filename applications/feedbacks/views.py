from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import FeedbackOnCustomerSerializer, FeedbackOnExecutorSerializer
from .permissions import IsCustomerPermission, IsExecutorPermission
from .models import FeedbackOnCustomer, FeedbackOnExecutor


@api_view(["POST"])
@permission_classes([IsCustomerPermission])
def create_feedback_on_executor(request):
    serializer = FeedbackOnExecutorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsExecutorPermission])
def create_feedback_on_customer(request):
    # Получить текущего исполнителя (предполагается, что вы авторизованы как исполнитель)
    executor = request.user.executor_profile

    # Добавить executor к данным обратной связи перед созданием
    feedback_data = request.data.copy()
    feedback_data["executor"] = executor.id  # Подставить id исполнителя

    serializer = FeedbackOnCustomerSerializer(data=feedback_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_feedbacks_view(request):
    user = request.user

    if user.role == "executor":
        # Если пользователь - исполнитель, получите список отзывов о нем
        feedbacks = FeedbackOnExecutor.objects.filter(executor=user.executor_profile)
        serializer = FeedbackOnExecutorSerializer(feedbacks, many=True)
    elif user.role == "customer":
        # Если пользователь - заказчик, получите список отзывов от него
        feedbacks = FeedbackOnCustomer.objects.filter(customer=user.customer_profile)
        serializer = FeedbackOnCustomerSerializer(feedbacks, many=True)
    else:
        # Если пользователь не имеет роли, верните пустой список
        serializer = []

    return Response(serializer.data)
