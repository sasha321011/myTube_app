from rest_framework import routers
from django.urls import path
from service.views import VideosViewSet, RatingCreateViewSet, CommentCreateViewSet, VideoCreateViewSet

urlpatterns = [
    path("api/video", VideosViewSet.as_view({"get": "list"})),
    path("api/video/<slug:slug>", VideosViewSet.as_view({"get": "retrieve"})),
    path("api/rate", RatingCreateViewSet.as_view({"post": "create"})),
    path("api/com", CommentCreateViewSet.as_view({"post": "create"})),
    path("api/upload-video", VideoCreateViewSet.as_view({"post": "create"})),
]

router = routers.DefaultRouter()

# router.register(r'api/video/comments/list',AllCommentView)
# router.register(r'api/video/watch',OneVideoViewSet,basename='video')
urlpatterns += router.urls
