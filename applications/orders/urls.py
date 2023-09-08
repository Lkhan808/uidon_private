from django.urls import path
from .views import (
    create_order_view,
    create_order_response_view,
    assign_executor_to_order_view,
    list_orders_view,
    list_responses_for_order_view,
    order_detail_view,
    update_or_delete_order_view,
    close_order_view,
    add_to_favorite_view,
    remove_from_favorite_view,
    executor_favorite_view,
    customer_order_active_list_view,
    customer_order_close_list_view,
    customer_order_progress_list_view,
    customer_order_all_list_view,
    customer_order_without_responses_view,
    executor_assigned_view,
    executor_completed_view,
    executor_responses_view
)


urlpatterns = [

    path('order/list/', list_orders_view),
    path('order/<int:order_id>/detail/', order_detail_view),

    path('customer/create/order/', create_order_view),
    path('customer/update-or-delete/order/<int:order_id>/', update_or_delete_order_view),
    path('customer/order/assign-executor/<int:order_id>/', assign_executor_to_order_view),
    path('customer/order/responses/list/<int:order_id>/', list_responses_for_order_view),
    path('customer/order/all/list/', customer_order_all_list_view),
    path('customer/order/active/list/', customer_order_active_list_view),
    path('customer/order/close/list/', customer_order_close_list_view),
    path('customer/order/progress/list/', customer_order_progress_list_view),
    path('customer/order/without/responses/list/', customer_order_without_responses_view),

    path('executor/orders/favorite/list/', executor_favorite_view),
    path('executor/orders/responses/list/', executor_responses_view),
    path('executor/orders/assigned/list/', executor_assigned_view),
    path('executor/orders/completed/list/', executor_completed_view),
    path('executor/orders/close/', close_order_view),
    path('executor/add/order/response/', create_order_response_view),
    path('executor/add/order/favorite/', add_to_favorite_view),
    path('executor/delete/order/favorite/', remove_from_favorite_view),
]