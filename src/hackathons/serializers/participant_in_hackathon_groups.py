from rest_framework.serializers import ModelSerializer

from hackathons.models.groups_in_hackathon import GroupsInHackathon
from hackathons.models.participant_in_hackathon_groups import ParticipantInHackathonGroups


class ParticipantInHackathonGroupsSerializer(ModelSerializer):
    group = GroupsInHackathon(many=True)

    class Meta:
        model = ParticipantInHackathonGroups
        fields = "__all__"
