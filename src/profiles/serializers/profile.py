from rest_framework.serializers import (
    DateField,
    ModelSerializer,
)

from common.serializers import (
    SocialLinkSerializer,
    ToolSerializer,
    UsefulMaterialSerializer,
)
from profiles.models import Profile
from profiles.serializers.award import AwardSerializer
from profiles.serializers.city import CitySerializer
from profiles.serializers.hobby import HobbySerializer
from profiles.serializers.profile_role import ProfileRoleSerializer


class ProfileSerializer(ModelSerializer[Profile]):
    birth_date = DateField()
    city = CitySerializer()
    awards = AwardSerializer(many=True)
    favourite_materials = UsefulMaterialSerializer(many=True)
    hobbies = HobbySerializer(many=True)
    roles = ProfileRoleSerializer(many=True, source="profilerole_set")
    social_links = SocialLinkSerializer(many=True)
    tools = ToolSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"
