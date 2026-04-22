from django.contrib import admin
from .models import Student, Lesson, SessionReport, ActiveSession

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'class_number', 'english_level')
    list_filter = ('year', 'class_number')
    search_fields = ('name',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'target_grammar')
    list_filter = ('year',)
    search_fields = ('title', 'target_grammar')

@admin.register(SessionReport)
class SessionReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_student_class', 'lesson', 'date')
    list_filter = ('student__year', 'student__class_number', 'student')
    
    # Custom column function to display "1-2" nicely
    def get_student_class(self, obj):
        return f"{obj.student.year}-{obj.student.class_number}"
    
    get_student_class.short_description = "Grade/Class"

@admin.register(ActiveSession)
class ActiveSessionAdmin(admin.ModelAdmin):
    list_display = ('year', 'class_number', 'active_lesson', 'is_active')
    list_editable = ('is_active',)
