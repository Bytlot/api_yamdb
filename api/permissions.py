from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only owners of an object to edit.
    Note, this permission assumes there is an `author` attribute on the
    object that maps to an `auth.User` instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
