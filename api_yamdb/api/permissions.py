class CommentPermission(permissions.BasePermission):

    def has_permision(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)
