from django.urls import path
from applications.profiles.views import (
    my_profile_view,

    executor_list_view,
    executor_create_view,
    executor_detail_view,
    executor_path_delete_view,

    customer_list_view,
    customers_detail_view,
    customer_create_view,
    customer_path_delete_view,
)

urlpatterns = [
    path("my-profile/", my_profile_view),

    path("executor/list/", executor_list_view),
    path("executor/<int:pk>/", executor_detail_view),
    path("executor/create/", executor_create_view),
    path("executor/update-or-delete/", executor_path_delete_view),

    path("customers/", customer_list_view),
    path("customer/<int:pk>/", customers_detail_view),
    path("customer/create/", customer_create_view),
    path("customer/update-or-delete/", customer_path_delete_view),

]