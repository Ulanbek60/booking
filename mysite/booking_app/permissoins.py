from rest_framework import permissions


class CheckUserCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'simpleUser':
            return False
        return True

class CheckReviewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'simpleUser':
            return True
        return False


class CheckReviewEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user_name
