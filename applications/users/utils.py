from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        "access": str(access),
        "refresh": str(refresh)
    }
