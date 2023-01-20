from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from . import models


class PerkSerializer(ModelSerializer):
    class Meta:
        model = models.Perk
        exclude = (
            "created_at",
            "update_at",
        )


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = models.Experience
        fields = (
            "name",
            "country",
            "price",
        )


class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perk = PerkSerializer(read_only=True, many=True)

    class Meta:
        model = models.Experience
        exclude = (
            "created_at",
            "update_at",
        )
