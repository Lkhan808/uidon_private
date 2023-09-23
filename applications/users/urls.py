from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    sign_up_view,
    verify_email_view,
    sign_in_view,
    password_reset,
    password_reset_confirm,
    change_password_view,
    change_email_view,
    google_login
)

urlpatterns = [
    path('signup/', sign_up_view),
    path('signin/', sign_in_view),
    path('verify-email/<int:user_id>/<str:jwt>/', verify_email_view),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password-reset/', password_reset, name='password-reset'),
    path('password-reset/confirm/<str:uid>/<str:token>/', password_reset_confirm, name='password-reset-update'),
    path('change-password/', change_password_view, name='change-password'),
    path('change-email/', change_email_view, name='change-email'),
    path('google-callback/', google_login, name='google-auth')
    path('verify-back-email/<int:user_id>/<str:jwt>/', verify_email_view),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password-reset/', password_reset),
    path('password-back-reset/confirm/<str:uid>/<str:token>/', password_reset_confirm),
    path('change-password/', change_password_view),
    path('change-email/', change_email_view),
    path('google-callback/', google_login)
]