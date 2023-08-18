from django.urls import path
from .views import (
    create_order,
    create_order_response,
    assign_executor_to_order,
    leave_order_review,
    list_orders,
    list_responses_for_order,
    order_detail,
)
urlpatterns = [
    path('create-order/', create_order, name='create-order'),
    path('orders/', list_orders, name='list-orders'),
    path('order/create-response/', create_order_response, name='create-order-response'),

    path('order/<int:order_id>/assign-executor/', assign_executor_to_order, name='assign-executor-to-order'),
    path('order/<int:order_id>/', order_detail, name='order-detail'),
    path('response/<int:order_response_id>/leave-review/', leave_order_review, name='leave-order-review'),
    path('order/<int:order_id>/responses/', list_responses_for_order, name='list-responses-for-order'),
]

