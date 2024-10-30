from rest_framework.serializers import ModelSerializer

from profiles.models import Award


class AwardSerializer(ModelSerializer[Award]):

    class Meta:
        model = Award
        fields = "__all__"
