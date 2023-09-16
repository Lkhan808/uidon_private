from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
<<<<<<< HEAD
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
=======
from .views import sign_up_view, verify_email_view, sign_in_view, password_reset, password_reset_confirm,\
    change_password_view, change_email_view, google_login
>>>>>>> 0fece5f81ed9691c7bc57c322d86519eb6190b45

urlpatterns = [
    path('signup/', sign_up_view),
    path('signin/', sign_in_view),

    path('verify-email/<int:user_id>/<str:jwt>/', verify_email_view),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('password-reset/', password_reset, name='password-reset'),
    path('password-reset/confirm/<str:uid>/<str:token>/', password_reset_confirm, name='password-reset-update'),

    path('change-password/', change_password_view, name='change-password'),
    path('change-email/', change_email_view, name='change-email'),
<<<<<<< HEAD

=======
>>>>>>> 0fece5f81ed9691c7bc57c322d86519eb6190b45
    path('google-callback/', google_login, name='google-auth')
]

