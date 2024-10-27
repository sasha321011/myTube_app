from rest_framework.routers import DefaultRouter
from django.urls import path
from service.views import (
    VideosViewSet,
    RatingCreateViewSet,
    CommentCreateViewSet,
    VideoCreateViewSet,
    AuthorVideosViewSet,
    VideoDetailViewSet,
)

urlpatterns = []


router = DefaultRouter()
router.register(r"video", VideosViewSet, basename="video")
router.register(r"video-detail", VideoDetailViewSet, basename="video-detail")
router.register(r"rate", RatingCreateViewSet, basename="rate")
router.register(r"com", CommentCreateViewSet, basename="comment")
router.register(r"upload-video", VideoCreateViewSet, basename="upload-video")
router.register(r"author-videos", AuthorVideosViewSet, basename="author-videos")

urlpatterns += router.urls
