from rest_framework import permissions


class IsUserSelfPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            #                and request.user.is_admin)
            and request.user.role == "admin"
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsStaffAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorModeratorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator)
            )
        )
<<<<<<< HEAD


class CommentPermission(permissions.BasePermission):

    def has_permision(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method == 'GET'
        else:
            return (obj.author == request.user or
                    request.user.role in ['admin', 'moderator'])
=======
>>>>>>> 21a889ed5db3ee4569f723ffa3280885f5905b43
