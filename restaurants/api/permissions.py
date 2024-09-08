from rest_framework import permissions

# custom permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_owner

        return False


class IsOwnerOrIsEmployee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_owner or request.user.is_employee

        return False
