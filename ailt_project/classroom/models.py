from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    YEAR_CHOICES = [(1, 'Year 1'),(2, 'Year 2'),(3, 'Year 3'),]
    name = models.CharField(max_length=100)
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    class_number = models.IntegerField(default=1)
    hobbies = models.TextField()
    english_level = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return f"{self.name} ({self.year}-{self.class_number})"

class Lesson(models.Model):
    YEAR_CHOICES = [(1, 'Year 1'),(2, 'Year 2'),(3, 'Year 3'),]
    title = models.CharField(max_length=200)
    year = models.IntegerField(choices=YEAR_CHOICES, default=1, help_text="学年")
    target_grammar = models.TextField()

    def __str__(self):
        return f"[Year {self.year}] {self.title}"

class SessionReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mistakes_logged = models.TextField(help_text="会話内容")

    def __str__(self):
        return f"{self.student.name} - {self.lesson.title}"
    
class ActiveSession(models.Model):
    YEAR_CHOICES = [(1, 'Year 1'),(2, 'Year 2'),(3, 'Year 3'),]
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    class_number = models.IntegerField(default=1, verbose_name="Class")
    active_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True, verbose_name="State")

    def __str__(self):
        return f"{self.year}-{self.class_number} | {self.active_lesson.title}"
    