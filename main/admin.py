from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as AuthGroup
from .models import *


class UserAdminCustom(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'last_name', 'email', 'role']
    list_filter = ['role']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class MentorAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'point_limit']
    list_filter = ['course']
    search_fields = ['name', 'user__username']
    ordering = ['name']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_filter = ['active']
    search_fields = ['name']
    filter_horizontal = ['courses', 'mentors']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'group', 'points']
    list_filter = ['group']
    search_fields = ['name', 'user__username']
    ordering = ['name']
    readonly_fields = ('point_history',)


class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']
    list_filter = ['created_by']
    search_fields = ['title', 'created_by__name']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test']
    search_fields = ['text']


class StudentTestResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'score', 'taken_at']
    list_filter = ['test', 'student']
    search_fields = ['student__name', 'test__title']


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'answer', 'is_correct']
    search_fields = ['answer', 'result__student__name']
    list_filter = ['is_correct']


class GivePointAdmin(admin.ModelAdmin):
    list_display = ['student', 'mentor', 'amount', 'point_type', 'date', 'created_at']
    list_filter = ['point_type', 'mentor']
    search_fields = ['student__name', 'mentor__name']
    readonly_fields = ('created_at',)

try:
    admin.site.unregister(AuthGroup)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdminCustom)
admin.site.register(Course)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(StudentTestResult, StudentTestResultAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(GivePoint, GivePointAdmin)
