from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from service.models import Video
from service.serializers import VideoSerializer


class VideoView(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer