from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import sign_up_view, verify_email_view, sign_in_view

urlpatterns = [
    path('sign-up/', sign_up_view),
    path('verify-email/<int:user_id>/<str:jwt>/', verify_email_view),
    path('sign-in/', sign_in_view),
    path('token/refresh/', TokenRefreshView.as_view()),
]

