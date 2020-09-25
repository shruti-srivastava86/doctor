from rest_framework import serializers

from doctor.video.models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = [
            "file"
        ]
