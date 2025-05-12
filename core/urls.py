
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import token_obtain_pair , token_refresh
from main.views import *

from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Euro Coin API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('token/', token_obtain_pair ),
    path('token/refresh/', token_refresh ),
]

urlpatterns += [
    path('users/get-me/', UserDetailView.as_view(), name='user-details'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/create/', CourseCreateView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view()),
    path('groups/', GroupListCreateView.as_view(), name='groups'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyView.as_view()),
    path('mentors/', MentorListCreateView.as_view(), name='mentors'),
    path('mentors/<int:pk>/', MentorRetrieveUpdateDestroyView.as_view()),
    path('mentors/get-me/', MentorDetailView.as_view(), name='mentor-details'),
    path('students/', StudentListCreateView.as_view(), name='students'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view()),
    path('students/get-me/', StudentDetailView.as_view(), name='student-details'),
    path('give-points/', GivePointCreateView.as_view()),
    path('give-points/list/', GivePointListView.as_view(), name='give_points'),
    path('give-points/<int:pk>/', GivePointRetrieveUpdateDestroyView.as_view()),

    path('test/' , TestListView.as_view(), name='test-list'),
    path('test/create/' , TestCreatView.as_view(),),
    path('test/<int:pk>/', TestRetrieveUpdateDestroyView.as_view()),
    path('students/test/result/', StudentTestResultListCreateView.as_view(), name='test-result'),
    path('student/test/result/<int:pk>' , StudentTestResultRetrieveUpdateDestroyView.as_view()),
    path('student/test/result/get-me/', StudentTestDetailView.as_view(), name='test-result-get-me'),
    path('students/answer/', StudentAnswerListView.as_view(), name='test-answer'),
    path('students/answer/create/', StudentAnswerCreateView.as_view(),),
    path('student/answer/<int:pk>/', StudentAnswerRetrieveUpdateDestroyView.as_view()),

    path('quesion/option/create/' , QuestionWithOptionsCreateView.as_view(), name='question-with-options'),
    path('quesion/' , QuestionListView.as_view(), name='question-list'),
    path('quesion/<int:pk>/' , QuestionRetrieveUpdateDestroyView.as_view()),
    path('quesion/create/', QuestionCreateView.as_view(), name='question-create'),

    path('answer/', AnswerOptionListView.as_view(), name='answer-option-list'),
    path('answer/create/', AnswerOptionCreateView.as_view(), name='answer-option-create'),
    path('answer/<int:pk>/' , AnswerOptionRetrieveUpdateDestroyView.as_view()),

    path('achievement/' , AchievementListCreateView.as_view(), name='achievement-list'),
    path('achievement/<int:pk>/' ,AchievementRetrieveUpdateDestroyView.as_view() ),
    path('api/tests/submit/', SubmitTestAPIView.as_view(), name='submit-test'),
    path('api/test-submission-log/', TestSubmissionLogAPIView.as_view(), name='test-submission-log'),


]
