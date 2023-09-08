from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import FeedbackOnCustomerSerializer, FeedbackOnExecutorSerializer
from .permissions import IsCustomerPermission, IsExecutorPermission


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
    serializer = FeedbackOnCustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)