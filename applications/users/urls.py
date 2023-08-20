from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import sign_up_view, verify_email_view, sign_in_view, password_reset, password_reset_confirm

urlpatterns = [
    path('signup/', sign_up_view),
    path('verify-email/<int:user_id>/<str:jwt>/', verify_email_view),
    path('signin/', sign_in_view),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password-reset/', password_reset, name='password-reset'),
    path('password-reset/confirm/', password_reset_confirm, name='password-reset-update'),
]

