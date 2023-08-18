from django.urls import path
from applications.profiles import views

urlpatterns = [
    path("executors/list/", views.get_executors_view),
    path("executors/create/", views.create_executor_view),
    path("executor/<int:pk>/detail/", views.get_executor_view),
    path("executors/<int:pk>/delete/", views.delete_executor_view),
]
