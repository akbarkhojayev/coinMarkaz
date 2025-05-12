from django.contrib import admin
from .models import Group as CustomGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.contrib.auth.models import Group

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

@admin.register(CustomGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'get_mentors', 'get_courses')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('-name',)

    def get_mentors(self, obj):
        return ", ".join([mentor.name for mentor in obj.mentors.all()])
    get_mentors.short_description = 'Mentors'

    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])
    get_courses.short_description = 'Courses'


class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    list_display = ('username', 'role', 'is_staff', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Course, CourseAdmin)


class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'point_limit', 'get_courses', 'birthday')
    search_fields = ('name', 'user__username')
    list_filter = ('point_limit', 'birthday')

    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.course.all()])
    get_courses.short_description = 'Courses'

admin.site.register(Mentor, MentorAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'points', 'group', 'get_mentor', 'created_at')
    search_fields = ('name', 'user__username', 'group__name')
    list_filter = ('group__name', 'created_at', )
    ordering = ('-created_at',)

    def get_mentor(self, obj):
        return ", ".join([mentor.name for mentor in obj.group.mentors.all()])
    get_mentor.short_description = 'Mentors'

admin.site.register(Student, StudentAdmin)



class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True
    inlines = [AnswerOptionInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "duration_minutes", "created_at")
    search_fields = ('title', 'created_by__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [QuestionInline]


from django.contrib.admin import SimpleListFilter

class AnswerCountFilter(SimpleListFilter):
    title = 'Answer count'
    parameter_name = 'answer_count'

    def lookups(self, request, model_admin):
        return (
            ('lt4', 'Less than 4'),
            ('eq4', 'Exactly 4'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'lt4':
            return [q for q in queryset if q.answeroption_set.count() < 4]
        if self.value() == 'eq4':
            return [q for q in queryset if q.answeroption_set.count() == 4]
        return queryset

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("test", "answer_count", "text")
    search_fields = ('text', 'test__title')
    list_filter = ("test__title", AnswerCountFilter)
    ordering = ('test',)
    inlines = [AnswerOptionInline]

    def answer_count(self, obj):
        return obj.options.count()
    answer_count.short_description = "Answers"

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('label', 'text', 'is_correct', 'question')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct', 'question__test__title')
    ordering = ('label',)

admin.site.register(AnswerOption, AnswerOptionAdmin)


class StudentTestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'taken_at')
    search_fields = ('student__name', 'test__title')
    list_filter = ('test__created_at',)
    ordering = ('-taken_at',)


admin.site.register(StudentTestResult, StudentTestResultAdmin)

class GivePointAdmin(admin.ModelAdmin):
    list_display = ('student', 'mentor', 'amount', 'point_type', 'created_at')
    search_fields = ('student__name', 'mentor__name')
    list_filter = ('point_type', 'created_at')
    ordering = ('-created_at',)


admin.site.register(GivePoint, GivePointAdmin)

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'point_price', 'image')
    search_fields = ('name',)
    ordering = ('-amount',)

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(TestSubmissionLog)

