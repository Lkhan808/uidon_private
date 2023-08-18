from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Ordering
from .serializers import OrderSerializer, OrderingSerializer
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

class OrderChooseExecutorView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        executor_id = request.data.get("executor_id")
        if executor_id is None:
            return Response({"error": "executor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            executor = ExecutorProfile.objects.get(pk=executor_id)
        except ExecutorProfile.DoesNotExist:
            return Response({"error": "Executor not found"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = "in_progress"
        instance.save()

        Ordering.objects.create(order=instance, executor=executor, attached=True)

        return Response({"message": "Executor has been chosen and orders status updated"}, status=status.HTTP_200_OK)
