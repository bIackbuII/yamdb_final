from rest_framework import permissions

from reviews.models import User


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in (User.ADMIN, User.MODERATOR)
                or obj.author == request.user
                or request.user.is_superuser
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == User.ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.role == User.ADMIN)


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role == User.ADMIN
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.role == User.ADMIN
                or request.user == obj)
