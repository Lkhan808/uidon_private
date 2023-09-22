from rest_framework import permissions


class IsCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer_profile')


class IsExecutorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'executor_profile')