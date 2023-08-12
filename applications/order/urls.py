from django.urls import path
from .views import OrderListView, OrderDetailView, OrderApplyView, OrderAppliedListView, OrderChooseExecutorView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('apply-order/', OrderApplyView.as_view(), name='apply-order'),
    path('applied-orders/', OrderAppliedListView.as_view(), name='applied-orders'),
    path('choose-executor/<int:pk>/', OrderChooseExecutorView.as_view(), name='choose-executor'),
]
