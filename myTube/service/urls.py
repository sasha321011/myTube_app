from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from service.views import (
    VideosListViewSet,
    RatingCreateViewSet,
    CommentCreateViewSet,
    VideoCreateViewSet,
    AuthorVideosViewSet,
    VideoDetailViewSet,
)

router = DefaultRouter()
router.register(r"video", VideosListViewSet, basename="video")
router.register(r"rate", RatingCreateViewSet, basename="rate")
router.register(r"com", CommentCreateViewSet, basename="comment")
router.register(r"upload-video", VideoCreateViewSet, basename="upload-video")
# router.register(r"author-videos", AuthorVideosViewSet, basename="author-videos")

urlpatterns = [
    path(
        "video-detail/<slug:slug>/",
        VideoDetailViewSet.as_view({"get": "retrieve"}),
        name="video-detail",
    ),
    path(
        "author-videos/<str:author>/",
        AuthorVideosViewSet.as_view({"get": "list"}),
        name="author-videos",
    ),

]

urlpatterns += router.urls
