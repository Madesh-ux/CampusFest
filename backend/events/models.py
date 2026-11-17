from django.db import models
from django.conf import settings
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to='event_images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    registration_type = models.CharField(
    max_length=20,
    choices=[
        ('INDIVIDUAL', 'Individual'),
        ('TEAM', 'Team'),
    ],
    default='INDIVIDUAL'
    )

    min_team_size = models.PositiveIntegerField(default=1)

    max_team_size = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Team(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='teams'
    )

    team_name = models.CharField(max_length=100)

    captain = models.ForeignKey(
        'accounts.StudentRecord',
        on_delete=models.PROTECT,
        related_name='captained_teams'
    )

    registered_by = models.ForeignKey(
        'accounts.StudentRecord',
        on_delete=models.PROTECT,
        related_name='submitted_team_registrations'
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'
    )

    student = models.ForeignKey(
        'accounts.StudentRecord',
        on_delete=models.PROTECT,
        related_name='team_memberships'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'student'],
                name='unique_student_in_team'
            )
        ]

    def __str__(self):
        return f"{self.student.student_id} - {self.team.team_name}"

class IndividualRegistration(models.Model):

    student = models.ForeignKey(
        'accounts.StudentRecord',
        on_delete=models.PROTECT,
        related_name='individual_registrations'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='individual_registrations'
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'event'],
                name='unique_individual_event_registration'
            )
        ]

    def __str__(self):
        return f"{self.student.student_id} - {self.event.name}"