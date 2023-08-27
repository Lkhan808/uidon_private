from django.urls import path
from .views import (
    create_order,
    create_order_response,
    assign_executor_to_order,
    list_orders,
    list_responses_for_order,
    order_detail,
    close_order_view,
    executor_orders_view
)
urlpatterns = [
    path('create-order/', create_order, name='create-order'),
    path('orders/', list_orders, name='list-orders'),
    path('order/<int:order_id>/', order_detail, name='order-detail'),
    path('order/respond-to-order/', create_order_response, name='create-order-response'),
    path('order/<int:order_id>/responses/', list_responses_for_order, name='list-responses-for-order'),
    path('order/<int:order_id>/assign-executor/', assign_executor_to_order, name='assign-executor-to-order'),
    path('executor/orders/', executor_orders_view, name='executor-orders'),
    path('executor/orders/<int:order_id>/close/', close_order_view, name='close-order'),

]

