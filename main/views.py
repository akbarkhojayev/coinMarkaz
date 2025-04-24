from django.shortcuts import  get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.permissions import *
from main.serializers import *
from django.http import Http404


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class MentorListCreateView(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]

class MentorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class MentorDetailView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsMentor]

    def get_object(self):
        return get_object_or_404(Mentor, user=self.request.user)

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        return Student.objects.get(user=self.request.user)

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StudentUpdateSerializer
        return StudentSerializer

class GivePointListCreateView(generics.ListCreateAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsAuthenticated]

class GivePointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsAuthenticated]

class TestListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

class TestCreatView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsMentorOrAdmin]

class TestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsMentorOrAdmin]


class StudentTestListView(ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'STUDENT':
            student = Student.objects.get(user=user)
            group_mentors = student.group.mentors.all()
            return Test.objects.filter(created_by__in=group_mentors)
        return Test.objects.none()


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class AnswerOptionListView(generics.ListAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsAuthenticated]

class AnswerOptionCreateView(generics.CreateAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsAuthenticated]

class AnswerOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsMentorOrAdmin]


class StudentTestResultListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentTestResult.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)

class StudentTestResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentTestResult.objects.filter(student__user=self.request.user)


class StudentTestDetailView(generics.RetrieveAPIView):
    serializer_class = StudentTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = StudentTestResult.objects.filter(
            student__user=self.request.user
        ).order_by('-taken_at').first()

        if obj is None:
            raise Http404("Oxirgi ishlagan test natijasi topilmadi.")
        return obj

class StudentAnswerListView(generics.ListAPIView):
    serializer_class = StudentAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentAnswer.objects.filter(result__student__user=self.request.user)


class StudentAnswerCreateView(generics.CreateAPIView):
    serializer_class = StudentAnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = StudentAnswer.objects.all()

class StudentAnswerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentAnswer.objects.filter(result__student__user=self.request.user)

class AchievementListCreateView(generics.ListCreateAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class AchievementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAdmin]

class SubmitTestView(generics.CreateAPIView):
    serializer_class = SubmitTestSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}