from rest_framework.routers import DefaultRouter
from django.urls import path
from service.views import (
    VideosViewSet,
    RatingCreateViewSet,
    CommentCreateViewSet,
    VideoCreateViewSet,
)


urlpatterns = []

router = DefaultRouter()
router.register(r"api/video", VideosViewSet, basename="video")
router.register(r"api/rate", RatingCreateViewSet, basename="rate")
router.register(r"api/com", CommentCreateViewSet, basename="comment")
router.register(r"api/upload-video", VideoCreateViewSet, basename="upload-video")

urlpatterns = router.urls
