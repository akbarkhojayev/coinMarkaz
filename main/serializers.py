from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','role')
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'birth_date', 'image','bio']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    course_names = serializers.SerializerMethodField()
    my_test = serializers.SerializerMethodField()
    my_group_id = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = ['id', 'name', 'birthday', 'image', 'point_limit', 'course_names', 'my_test' , 'my_group_id']

    def get_course_names(self, obj):
        return [course.name for course in obj.course.all()]

    def get_my_test(self, obj):
        tests = Test.objects.filter(created_by=obj)
        return [{"id": test.id,"title": test.title, "description": test.description} for test in tests]

    def get_my_group_id(self, obj):
        return list(Group.objects.filter(mentors=obj).values_list('id', flat=True))


class MentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['name', 'image' , 'birthday']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class StudentTestResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    test_title = serializers.SerializerMethodField()

    class Meta:
        model = StudentTestResult
        fields = '__all__'
        read_only_fields = ['score', 'taken_at']

    def get_student_name(self, obj):
        return obj.student.name

    def get_test_title(self, obj):
        return obj.test.title

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'
        read_only_fields = ['is_correct']

    def create(self, validated_data):
        answer_option = validated_data['answer_option']
        validated_data['is_correct'] = answer_option.is_correct
        instance = super().create(validated_data)

        result = instance.result
        result.update_score()

        return instance


class GivePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = GivePoint
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    test_description = serializers.SerializerMethodField()
    test_title = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'text', 'test_description', 'test_title', 'test']

    def get_test_description(self, obj):
        return obj.test.description

    def get_test_title(self, obj):
        return obj.test.title

class AnswerOptionSerializer(serializers.ModelSerializer):
    test_id = serializers.SerializerMethodField()
    question_text = serializers.SerializerMethodField()

    class Meta:
        model = AnswerOption
        fields = ['id', 'question', 'question_text', 'test_id', 'label', 'text', 'is_correct']

    def get_test_id(self, obj):
        return obj.question.test.id

    def get_question_text(self, obj):
        return obj.question.text

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'students']

    def get_students(self, obj):
        students = Student.objects.filter(group__courses=obj)
        return students.values('id', 'name')


class AnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_option_id = serializers.IntegerField()

class SubmitTestSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    answers = AnswerSubmissionSerializer(many=True)

    def validate(self, attrs):
        test_id = attrs.get('test_id')
        answers = attrs.get('answers')

        if not answers:
            raise serializers.ValidationError({"answers": "You must provide at least one answer."})

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise serializers.ValidationError({"test_id": "Test not found."})

        for answer in answers:
            try:
                question = Question.objects.get(id=answer['question_id'], test=test)
            except Question.DoesNotExist:
                raise serializers.ValidationError(
                    {"question_id": f"Question {answer['question_id']} not found in this test."})

            try:
                option = AnswerOption.objects.get(id=answer['answer_option_id'], question=question)
            except AnswerOption.DoesNotExist:
                raise serializers.ValidationError({
                                                      "answer_option_id": f"Answer option {answer['answer_option_id']} does not belong to question {answer['question_id']}."})

        return attrs

    def create(self, validated_data):
        student = self.context['request'].user.student
        test = Test.objects.get(id=validated_data['test_id'])

        if StudentTestResult.objects.filter(student=student, test=test).exists():
            raise serializers.ValidationError("You have already submitted this test.")

        answers = validated_data['answers']
        if not answers:
            raise serializers.ValidationError({"answers": "You must provide at least one answer."})

        result = StudentTestResult.objects.create(student=student, test=test)

        for answer in validated_data['answers']:
            question = Question.objects.get(id=answer['question_id'])
            option = AnswerOption.objects.get(id=answer['answer_option_id'])
            StudentAnswer.objects.create(result=result, question=question, answer_option=option)

        result.update_score()
        return result
