from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Event
from .serializers import EventSerializer

#Individual Regestration views
from django.db import IntegrityError, transaction
from rest_framework.permissions import IsAuthenticated
from .models import IndividualRegistration
from .serializers import IndividualRegistrationSerializer
from accounts.models import StudentRecord

from .models import Team, TeamMember
from .serializers import TeamRegistrationSerializer


class EventListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        events = Event.objects.filter(is_active=True)

        search = request.query_params.get('search')

        category = request.query_params.get('category')

        if search:
            events = events.filter(name__icontains=search)

        if category:
            events = events.filter(category__iexact=category)

        serializer = EventSerializer(events, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class EventDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:
            event = Event.objects.get(
                id=pk,
                is_active=True
            )

        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(event)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class IndividualRegistrationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = IndividualRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        event_id = serializer.validated_data['event_id']

        event = Event.objects.filter(
            id=event_id,
            is_active=True
        ).first()

        if event is None:
            return Response(
                {"error": "Event not found or inactive"},
                status=status.HTTP_404_NOT_FOUND
            )

        if event.registration_type != 'INDIVIDUAL':
            return Response(
                {"error": "This event requires team registration"},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = StudentRecord.objects.filter(
            user=request.user
        ).first()

        if student is None:
            return Response(
                {"error": "Student record not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():

                registration, created = IndividualRegistration.objects.get_or_create(
                    student=student,
                    event=event
                )

        except IntegrityError:
            return Response(
                {"error": "Registration failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not created:
            return Response(
                {"error": "You have already registered for this event"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Event registration successful"},
            status=status.HTTP_201_CREATED
        )

class TeamRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TeamRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        event = Event.objects.filter(
            id=data['event_id'],
            is_active=True
        ).first()

        if event is None:
            return Response({"error": "Event not found"}, status=404)

        if event.registration_type != 'TEAM':
            return Response({"error": "This is not a team event"}, status=400)

        student_ids = data['member_student_ids']

        if len(student_ids) < event.min_team_size or len(student_ids) > event.max_team_size:
            return Response({"error": "Invalid team size"}, status=400)

        students = StudentRecord.objects.filter(student_id__in=student_ids)

        if students.count() != len(student_ids):
            return Response({"error": "Invalid student IDs"}, status=400)

        captain = students.get(student_id=data['captain_student_id'])

        registered_by = StudentRecord.objects.filter(user=request.user).first()

        if registered_by is None or registered_by not in students:
            return Response({"error": "You must be a team member to register"}, status=400)

        if TeamMember.objects.filter(
            student__in=students,
            team__event=event
        ).exists():
            return Response({"error": "A student is already registered in another team"}, status=400)

        team = Team.objects.create(
            event=event,
            team_name=data['team_name'],
            captain=captain,
            registered_by=registered_by
        )

        TeamMember.objects.bulk_create([
            TeamMember(team=team, student=student)
            for student in students
        ])

        return Response(
            {"message": "Team registration successful"},
            status=201
        )