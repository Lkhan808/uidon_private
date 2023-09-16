from rest_framework import permissions

class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений для проверки, имеет ли пользователь доступ на изменение заказа.
    """

    def has_permission(self, request, view):
        # Разрешено только чтение (GET) для всех, даже неавторизованных пользователей.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли текущий пользователь заказчиком (customer).
        return hasattr(request.user, 'customer_profile')

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True  # Разрешаем GET-запросы без дополнительной проверки.

        # Проверяем, является ли текущий пользователь заказчиком.
        return hasattr(request.user, 'customer_profile')

class IsCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли текущий пользователь заказчиком (customer).
        return hasattr(request.user, 'customer_profile')

class IsExecutorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'executor_profile')


def addcwe():
    pass