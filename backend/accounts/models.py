from django.db import models
from django.conf import settings

class StudentRecord(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    is_claimed = models.BooleanField(default=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,blank=True,
        related_name='student_record'
    )

    def __str__(self):
        return self.student_id