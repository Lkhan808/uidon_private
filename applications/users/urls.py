from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import SimpleRouter
from .views import (
    SignUpView,
    VerifyEmailView,
    SignInView,
    ExecutorViewSet,
    CustomerViewSet
)

router = SimpleRouter()
router.register(r"executors", ExecutorViewSet, basename="executor")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/<int:user_id>/<str:jwt>/', VerifyEmailView.as_view(), name='verify-email'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('token/refresh/', TokenRefreshView.as_view()),
]

urlpatterns += router.urls