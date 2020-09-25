from rest_framework import serializers

from doctor.badges.models import Badges


class BadgesSerializer(serializers.ModelSerializer):
    """
        Serializer for badges.
    """
    class Meta:
        model = Badges
        exclude = [
            "created_at",
            "updated_at",
            "description"
        ]
