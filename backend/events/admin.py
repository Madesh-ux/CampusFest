from django.contrib import admin
from .models import Event, Team, TeamMember,IndividualRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'date',
        'venue',
        'registration_type',
        'min_team_size',
        'max_team_size',
        'is_active'
    )

    search_fields = ('name', 'category', 'venue')

    list_filter = ('category', 'registration_type', 'is_active')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'team_name',
        'event',
        'captain',
        'registered_by',
        'registered_at'
    )

    search_fields = ('team_name', 'captain__student_id')

    list_filter = ('event',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'student', 'joined_at')

    search_fields = ('student__student_id', 'team__team_name')

@admin.register(IndividualRegistration)
class IndividualRegistrationAdmin(admin.ModelAdmin):

    list_display = ('student', 'event', 'registered_at')

    search_fields = ('student__student_id', 'event__name')

    list_filter = ('event',)