from rest_framework.permissions import BasePermission
from main.models import Mentor, Student


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Mentor.objects.filter(user=request.user).exists()

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Student.objects.filter(user=request.user).exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsMentorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (Mentor.objects.filter(user=request.user).exists() or request.user.is_superuser)
