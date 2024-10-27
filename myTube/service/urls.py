from rest_framework.routers import DefaultRouter
from django.urls import path
from service.views import (
    VideosViewSet,
    RatingCreateViewSet,
    CommentCreateViewSet,
    VideoCreateViewSet,
    AuthorVideosViewSet,
    VideoDetailViewSet
)
urlpatterns = [
    
]



router = DefaultRouter()
router.register(r"api/video", VideosViewSet, basename="video")
router.register(r"api/video-detail", VideoDetailViewSet, basename="video-detail")
router.register(r"api/rate", RatingCreateViewSet, basename="rate")
router.register(r"api/com", CommentCreateViewSet, basename="comment")
router.register(r"api/upload-video", VideoCreateViewSet, basename="upload-video")
router.register(r"api/author-videos", AuthorVideosViewSet, basename="author-videos")

urlpatterns += router.urls
