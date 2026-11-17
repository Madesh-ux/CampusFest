from django.contrib import admin
from .models import StudentRecord


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'is_claimed')
    search_fields = ('student_id', 'first_name', 'last_name')
    list_filter = ('is_claimed',)