from rest_framework.serializers import ModelSerializer

from profiles.models import ProfileRole


class ProfileRoleSerializer(ModelSerializer[ProfileRole]):

    class Meta:
        model = ProfileRole
        fields = "__all__"
