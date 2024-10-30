from rest_framework.serializers import ModelSerializer

from hackathons.models.hackathon_participation_request import HackathonParticipationRequest


class HackathonParticipationRequestSerializer(ModelSerializer):
    class Meta:
        model = HackathonParticipationRequest
        fields = "__all__"
