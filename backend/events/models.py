from django.db import models

# Create your models here.
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