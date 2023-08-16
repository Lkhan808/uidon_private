from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderAppliedListView,
    OrderChooseExecutorView,
    OrderResponseView
)


urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('applied-orders/', OrderAppliedListView.as_view(), name='applied-orders'),
    path('choose-executor/<int:pk>/', OrderChooseExecutorView.as_view(), name='choose-executor'),
    path('respond-to-order/', OrderResponseView.as_view(), name='respond-to-order'),
]
