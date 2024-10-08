from rest_framework import serializers

from service.models import Video


class VideoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    #email = serializers.CharField(source='author.email')

    class Meta:
        model = Video
        fields = ('name','slug','created_at','tags','length_time','pre_view','author','username')