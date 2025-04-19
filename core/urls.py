
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
    path('courses/', CourseListCreateView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view()),
    path('groups/', GroupListCreateView.as_view(), name='groups'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyView.as_view()),
    path('mentors/', MentorListCreateView.as_view(), name='mentors'),
    path('mentors/<int:pk>/', MentorRetrieveUpdateDestroyView.as_view()),
    path('mentors/get-me/', MentorDetailView.as_view(), name='mentor-details'),
    path('students/', StudentListCreateView.as_view(), name='students'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view()),
    path('students/get-me/', StudentDetailView.as_view(), name='student-details'),
    path('give-points/', GivePointListCreateView.as_view(), name='give_points'),
    path('give-points/<int:pk>/', GivePointRetrieveUpdateDestroyView.as_view()),
]
