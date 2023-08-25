from django.urls import path
from .views import create_feedback_on_customer, create_feedback_on_executor

urlpatterns = [
    path('create_feedback_on_customer/', create_feedback_on_customer, name='create_feedback_on_customer'),
    path('create_feedback_on_executor/', create_feedback_on_executor, name='create_feedback_on_executor'),
]
