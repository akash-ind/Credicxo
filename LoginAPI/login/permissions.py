from rest_framework import permissions
from django.contrib.auth.models import Group


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Authorizes only teachers and Admin to work
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        admin = Group.objects.get(name = "admin")
        teacher = Group.objects.get(name = "teacher")
        if admin in user.groups.all():
            return True
        elif teacher in user.groups.all():
            return True
        return False


class IsAdmin(permissions.BasePermission):
    """
    Authorizes only Admin to work
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        admin = Group.objects.get(name = "admin")
        if admin in user.groups.all():
            return True
        return False
        