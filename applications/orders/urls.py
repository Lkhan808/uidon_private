from django.urls import path
from .views import (
    create_order_view,
    create_order_response_view,
    assign_executor_to_order_view,
    list_orders_view,
    list_responses_for_order_view,
    order_detail_view,
    close_order_view,
    add_to_favorite_view,
    remove_from_favorite_view,
    executor_favorite_view,
    customer_orders_list_view,
    customer_close_orders_list_view,
    executor_assigned_view,
    executor_completed_view,
    executor_responses_view
)




urlpatterns = [
    path('create-order/', create_order_view, name='create-order'),
    path('orders/', list_orders_view, name='list-orders'),
    path('order/<int:order_id>/', order_detail_view, name='order-detail'),

    path('order/<int:order_id>/responses/', list_responses_for_order_view, name='list-responses-for-order'),
    path('order/<int:order_id>/assign-executor/', assign_executor_to_order_view, name='assign-executor-to-order'),

    path('executor/orders/favorite/list/', executor_favorite_view, name='executor-orders-favorite-list'),
    path('executor/orders/response/list/', executor_responses_view, name='executor-orders-response-list'),
    path('executor/orders/assigned/list/', executor_assigned_view, name='executor-orders-assigned-list'),
    path('executor/orders/completed/list/', executor_completed_view, name='executor-orders-completed-list'),
    path('executor/orders/<int:order_id>/close/', close_order_view, name='executor-orders-close'),
    path('executor/add/order/respond/', create_order_response_view, name='create-order-response'),
    path('executor/add/order/favorite/<int:order_id>/', add_to_favorite_view, name='executor-add-favorite'),
    path('executor/delete/favorite/<int:order_id>/', remove_from_favorite_view, name='remove-executor-favorites'),

    path('customer/orders/list/', customer_orders_list_view, name='customer-orders-list'),
    path('customer/close/orders/list/', customer_close_orders_list_view, name='customer-close-orders-list'),
]