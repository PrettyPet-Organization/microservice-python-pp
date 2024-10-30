from rest_framework.serializers import ModelSerializer

from profiles.models import City


class CitySerializer(ModelSerializer[City]):

    class Meta:
        model = City
        fields = "__all__"
