from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import StudentRecord
from .serializers import StudentRegistrationSerializer

#Authentication and tokens

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import StudentLoginSerializer

# Is Authenticated User
from rest_framework.permissions import IsAuthenticated

# Dashboard Api/ Registration Api
from events.models import IndividualRegistration, TeamMember


class StudentRegistrationView(APIView):

    def post(self, request):

        serializer = StudentRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        with transaction.atomic():

            student = StudentRecord.objects.select_for_update().filter(
                student_id=data['student_id']
            ).first()

            if student is None:
                return Response(
                    {"error": "Invalid student ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if student.is_claimed:
                return Response(
                    {"error": "This student ID has already been registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(email__iexact=data['email']).exists():
                return Response(
                    {"error": "Email is already registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data.get('last_name', '')
            )
            student.user = user
            student.is_claimed = True
            student.save(update_fields=['user', 'is_claimed'])

        return Response(
            {
                "message": "Registration successful",
                "user_id": user.id
            },
            status=status.HTTP_201_CREATED
        )

class StudentLoginView(APIView):

    def post(self, request):

        serializer = StudentLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )

class StudentProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = StudentRecord.objects.get(user=request.user)

        return Response({
            "student_id": student.student_id,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email
        })

class MyRegistrationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = StudentRecord.objects.get(user=request.user)

        individual = IndividualRegistration.objects.filter(
            student=student
        )

        teams = TeamMember.objects.filter(
            student=student
        )

        individual_data = [
            {
                "event": registration.event.name,
                "date": registration.event.date,
                "venue": registration.event.venue
            }
            for registration in individual
        ]

        team_data = [
            {
                "team": member.team.team_name,
                "event": member.team.event.name,
                "captain": member.team.captain.student_id,
                "date": member.team.event.date,
                "venue": member.team.event.venue
            }
            for member in teams
        ]

        return Response({
            "individual_registrations": individual_data,
            "team_registrations": team_data
        })