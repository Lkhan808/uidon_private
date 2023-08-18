from django.urls import path
from .views import OrderListView, OrderDetailView, OrderApplyView, OrderAppliedListView, OrderChooseExecutorView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders-detail'),
    path('apply-orders/', OrderApplyView.as_view(), name='apply-orders'),
    path('applied-orders/', OrderAppliedListView.as_view(), name='applied-orders'),
    path('choose-executor/<int:pk>/', OrderChooseExecutorView.as_view(), name='choose-executor'),
]
