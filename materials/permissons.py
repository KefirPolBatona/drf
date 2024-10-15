from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь модератором.
        """

        return request.user.groups.filter(name='moderator').exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь владельцем.
        """

        return obj.owner == request.user
