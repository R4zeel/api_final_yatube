from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверка авторства объекта для совершения дальнейших операций."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
    


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторства объекта для совершения дальнейших операций."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
                return True
        return obj.author == request.user