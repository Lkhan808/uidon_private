from django.urls import path
from .views import create_feedback_on_customer, create_feedback_on_executor, my_feedbacks_view

urlpatterns = [
    path('create_feedback_on_customer/', create_feedback_on_customer),
    path('create_feedback_on_executor/', create_feedback_on_executor),
    path('my-feedbacks/list/', my_feedbacks_view),
]
