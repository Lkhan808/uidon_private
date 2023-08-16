from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Ordering
from .serializers import (
    OrderSerializer,
    OrderingSerializer,
    OrderResponseSerializer,
    OrderChooseExecutorSerializer
)
from applications.users.models import ExecutorProfile


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderApplyView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderAppliedListView(generics.ListAPIView):
    queryset = Ordering.objects.all()
    serializer_class = OrderingSerializer

class OrderChooseExecutorView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderChooseExecutorSerializer

    def create(self, request, *args, **kwargs):
        executor_id = request.data.get("executor_id")
        order_id = request.data.get("order_id")

        if executor_id is None or order_id is None:
            return Response({"error": "executor_id and order_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            executor = ExecutorProfile.objects.get(pk=executor_id)
            order = Order.objects.get(pk=order_id)
        except ExecutorProfile.DoesNotExist:
            return Response({"error": "Executor not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "in_progress"
        order.save()

        Ordering.objects.create(order=order, executor=executor, attached=True)

        return Response({"message": "Executor has been chosen for the order and order status updated"},
                        status=status.HTTP_200_OK)


class OrderResponseView(generics.CreateAPIView):
    serializer_class = OrderResponseSerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        executor_id = request.data.get("executor_id")

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            executor = ExecutorProfile.objects.get(pk=executor_id)
        except ExecutorProfile.DoesNotExist:
            return Response({"error": "Executor not found"}, status=status.HTTP_400_BAD_REQUEST)

        response = Ordering.objects.create(order=order, executor=executor, attached=False)

        return Response({"message": "Response to order created", "response_id": response.id}, status=status.HTTP_201_CREATED)
