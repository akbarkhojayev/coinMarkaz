from django.shortcuts import  get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from main.permissions import *
from main.serializers import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status



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
    permission_classes = [IsMentorOrAdmin]

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsMentorOrAdmin]

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsMentorOrAdmin]

class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsMentorOrAdmin]


class MentorListCreateView(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsMentorOrAdmin]

class MentorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorUpdateSerializer
    permission_classes = [IsMentorOrAdmin]
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
    permission_classes = [IsMentorOrAdmin]

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

class GivePointListView(generics.ListAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsAuthenticated]

class GivePointCreateView(generics.CreateAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsMentorOrAdmin]

class GivePointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsMentorOrAdmin]

class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'STUDENT':
            student = Student.objects.get(user=user)
            return Test.objects.filter(groups=student.group)
        elif user.is_authenticated and user.role in ['ADMIN', 'TEACHER']:
            return Test.objects.all()
        return Test.objects.none()


class TestCreatView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsMentorOrAdmin]


class TestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsMentorOrAdmin]


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]

class AnswerOptionListView(generics.ListAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsAuthenticated]

class AnswerOptionCreateView(generics.CreateAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsMentorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

class AnswerOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsMentorOrAdmin]

class QuestionWithOptionsCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionWithOptionsSerializer
    permission_classes = [IsMentorOrAdmin]


class StudentTestResultListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentTestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'student'):
            # Student – faqat o‘z natijalarini ko‘radi
            return StudentTestResult.objects.filter(student=user.student)

        elif hasattr(user, 'mentor'):
            # Mentor – faqat o‘ziga biriktirilgan guruhlardagi o‘quvchilar natijalarini ko‘radi
            mentor = user.mentor

            # Mentorning guruhlari
            groups = Group.objects.filter(mentors=mentor)

            # Guruhlardagi o‘quvchilar
            students = Student.objects.filter(group__in=groups)

            return StudentTestResult.objects.filter(student__in=students)

        # Boshqa rollar uchun hech narsa
        return StudentTestResult.objects.none()

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
        obj = StudentTestResult.objects.filter(student__user=self.request.user).last()

        if obj is None:
            raise Http404("Sizga tegishli test natijasi topilmadi.")
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


class SubmitTestAPIView(APIView):
    def post(self, request):
        try:
            student = request.data.get("student")
            test = request.data.get("test")
            correct_count = request.data.get("correct_answers")

            if student in [None, ""] or test in [None, ""] or correct_count in [None, ""]:
                return Response({"error": "Ma'lumotlar to'liq emas"}, status=400)

            try:
                correct_count = int(correct_count)
            except ValueError:
                return Response({"error": "'correct_answers' butun son bo'lishi kerak"}, status=400)

            coin_amount = correct_count * 5

            student = get_object_or_404(Student, id=student)
            test = get_object_or_404(Test, id=test)

            result, created = StudentTestResult.objects.get_or_create(
                student=student,
                test=test,
                defaults={'score': coin_amount}
            )

            if not created:
                return Response({"detail": "Bu test allaqachon bajarilgan"}, status=400)

            student.points += coin_amount

            student.point_history.append({
                'amount': coin_amount,
                'point_type': 'test',
                'description': f"{test.title} testidan {correct_count} ta to‘g‘ri javob",
            })

            student.save()

            TestSubmissionLog.objects.create(
                student=student,
                test=test,
                correct_answers=correct_count
            )

            return Response({
                "detail": f"{correct_count} ta to‘g‘ri javob uchun {coin_amount} ball qo‘shildi",
                "total_points": student.points,
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TestSubmissionLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student
        logs = TestSubmissionLog.objects.filter(student=student)
        serializer = TestSubmissionLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TestSubmissionLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user.student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
