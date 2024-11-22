from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from service.views import (
    VideosListView,
    RatingCreateView,
    CommentCreateView,
    VideoCreateView,
    AuthorVideosView,
    VideoDetailView,
    RatedVideoView,
)

router = DefaultRouter()
router.register(r"video", VideosListView, basename="video")
router.register(r"rate", RatingCreateView, basename="rate")
router.register(r"com", CommentCreateView, basename="comment")
router.register(r"upload-video", VideoCreateView, basename="upload-video")
router.register(r"rated-videos", RatedVideoView, basename="rated-videos")
# router.register(r"author-videos", AuthorVideosViewSet, basename="author-videos")

urlpatterns = [
    path(
        "video-detail/<slug:slug>/",
        VideoDetailView.as_view({"get": "retrieve"}),
        name="video-detail",
    ),
    path(
        "author-videos/<str:author>/",
        AuthorVideosView.as_view({"get": "list"}),
        name="author-videos",
    ),

]

urlpatterns += router.urls
