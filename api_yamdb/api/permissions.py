<<<<<<< HEAD
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка на администратора
    """

    message = "Вы не являетесь администратором"

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == "admin"
        )
=======
class CommentPermission(permissions.BasePermission):

    def has_permision(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)
>>>>>>> comment
