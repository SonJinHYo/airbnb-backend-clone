from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerialzier


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerialzier(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
