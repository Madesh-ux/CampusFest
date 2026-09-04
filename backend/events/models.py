from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Event(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=50,choices=[('SPORTS','Sports'),
                                                     ('CULTURALS','Culturals'),
                                                     ("DJ NIGHT",'DJ Night')
                                                     ])
    description=models.TextField()
    rules=models.TextField()
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    venue=models.CharField(max_length=200)
    image=models.ImageField(upload_to='events/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    registration_id=models.CharField(max_length=20,unique=True)
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="event_registrations")
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name="registrations")
    registered_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["student","event"],name='unique_student_event')
        ]

    def __str__(self):
        return self.registration_id