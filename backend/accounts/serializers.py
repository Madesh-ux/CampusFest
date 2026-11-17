from rest_framework import serializers

class StudentRegistrationSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(
    max_length=100,
    required=False,
    allow_blank=True
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,min_length=8)

class StudentLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )