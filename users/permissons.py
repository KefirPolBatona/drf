from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        else:
            return request.user.is_authenticated
