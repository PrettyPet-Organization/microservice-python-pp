from rest_framework import serializers

from profiles.models import Hobby


class HobbySerializer(serializers.ModelSerializer[Hobby]):

    class Meta:
        model = Hobby
        fields = "__all__"
