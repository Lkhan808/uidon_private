from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView,
    VerifyEmailView,
    SignInView,
    ExecutorListView,
    ExecutorRetrieveView,
    CustomerListView,
    CustomerRetrieveView
)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/<int:user_id>/<str:jwt>/', VerifyEmailView.as_view(), name='verify-email'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('executors/', ExecutorListView.as_view()),
    path('executor/<int:pk>/', ExecutorRetrieveView.as_view()),
    path('customers/', CustomerListView.as_view()),
    path('customer/<int:pk>/', CustomerRetrieveView.as_view()),

]

