from rest_framework import serializers

from service.models import Video


class VideoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    #email = serializers.CharField(source='User.email')

    class Meta:
        model = Video
        fields = ('name','slug','created_at','length_time','pre_view','author','username')