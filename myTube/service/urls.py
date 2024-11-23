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
    MakeAuthorVideosListView,
    PlaylistLikeViewSet,
    AuthorPlaylistsViewSet,
    LikedPlaylistsViewSet,
    PlaylistVideosViewSet,
)

router = DefaultRouter()
router.register(r"video", VideosListView, basename="video")
router.register(r"rate", RatingCreateView, basename="rate")
router.register(r"com", CommentCreateView, basename="comment")
router.register(r"upload-video", VideoCreateView, basename="upload-video")
router.register(r"rated-videos", RatedVideoView, basename="rated-videos")
router.register(r"make-playlist", MakeAuthorVideosListView, basename="make-playlist")

router.register(r"liked-playlists", LikedPlaylistsViewSet, basename="liked-playlists")
router.register(r"like-playlist", PlaylistLikeViewSet, basename="like-playlist")

urlpatterns = [
    path(
        "video-detail/<slug:slug>/",
        VideoDetailView.as_view({"get": "retrieve"}),
        name="video-detail",
    ),
    path(
        "playlist-videos/<slug:slug>/",
        PlaylistVideosViewSet.as_view({"get": "list"}),
        name="playlist-videos",
    ),
    path(
        "author-playlists/<str:author>/",
        AuthorPlaylistsViewSet.as_view({"get": "list"}),
        name="author-playlists",
    ),
]


urlpatterns += router.urls
