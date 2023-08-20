from django.urls import path
from applications.profiles.views import (executors_list_view, executor_detail_view,
                                         customers_list_view, customer_detail_view)

urlpatterns = [
    path("executors/", executors_list_view),
    path("executor/<int:pk>/", executor_detail_view),
    path("customers/", customers_list_view),
    path("customer/<int:pk>/", customer_detail_view),
]