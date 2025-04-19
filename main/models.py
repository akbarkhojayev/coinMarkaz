from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    name = models.CharField(max_length=100)
    point_limit = models.IntegerField()
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"


class Group(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    mentors = models.ManyToManyField(Mentor)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    point_history = models.JSONField(default=list, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class StudentTestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    taken_at = models.DateTimeField(auto_now_add=True)

    def update_score(self):
        correct_count = self.answers.filter(is_correct=True).count()
        self.score = correct_count * 5
        self.save()

        if self.score > 0:
            self.student.point_history.append({
                'amount': self.score,
                'point_type': 'test',  # Points coming from a test
                'description': f"Points earned from test '{self.test.title}'",
                'date': self.taken_at,
            })
            self.student.save()

    def __str__(self):
        return f"{self.student.name} - {self.test.title} - {self.score} coins"

class StudentAnswer(models.Model):
    result = models.ForeignKey(StudentTestResult, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_correct = self.answer.strip().lower() == self.question.correct_answer.strip().lower()

        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and self.is_correct:
            self.result.student.points += 5
            self.result.student.save()

            # Add the "From Test" point to history
            self.result.student.point_history.append({
                'amount': 5,
                'point_type': 'test',
                'description': f"Correct answer for {self.question.text}",
                'date': self.result.taken_at,
            })
            self.result.student.save()

        self.result.update_score()

    def __str__(self):
        return f"{self.result.student.name} -> {self.question.text} = {self.answer}"

class GivePoint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True ,blank=True)
    point_type = models.CharField(max_length=20, choices=[('mentor', 'From Mentor'), ('test', 'From Test')], default='mentor')
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} {self.amount} -> {self.mentor.name}"

    def clean(self):
        if self.amount > self.mentor.point_limit:
            raise ValidationError(f"Mentor can give max {self.mentor.point_limit} points")


    def save(self, *args, **kwargs):
        self.student.points += self.amount
        self.student.point_history.append({
            'amount': self.amount,
            'point_type': self.point_type,
            'description': self.description,
            'date': self.date,
        })
        self.student.save()
        super().save(*args, **kwargs)
