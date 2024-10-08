
from rest_framework.viewsets import ReadOnlyModelViewSet

from service.models import Video
from service.serializers import VideoSerializer


class VideoView(ReadOnlyModelViewSet):
    queryset = Video.objects.all().prefetch_related('tags').select_related('author')
    serializer_class = VideoSerializer