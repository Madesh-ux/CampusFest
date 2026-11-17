from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class IndividualRegistrationSerializer(serializers.Serializer):

    event_id = serializers.IntegerField()

class TeamRegistrationSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()

    team_name = serializers.CharField(max_length=100)

    captain_student_id = serializers.CharField(max_length=30)

    member_student_ids = serializers.ListField(
        child=serializers.CharField(max_length=30),
        allow_empty=False
    )

    def validate_member_student_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate student IDs are not allowed."
            )

        return value

    def validate(self, data):
        if data['captain_student_id'] not in data['member_student_ids']:
            raise serializers.ValidationError(
                "Captain must be one of the team members."
            )

        return data