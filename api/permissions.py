from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
                   request.method in permissions.SAFE_METHODS or
                   request.user.is_authenticated and obj.author == request.user or  # noqa
                   request.user.is_admin or
                   request.user.is_moderator
                   )
