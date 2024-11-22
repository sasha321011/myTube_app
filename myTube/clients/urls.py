from rest_framework.routers import DefaultRouter
from clients.views import (
    SubscribeCreateDestroy,
    ProfileViewSet,
    SelectedUserViewSet,
    SubsUserViewSet,
)
from django.urls import path, include


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
]

router = DefaultRouter()
router.register(r"make-sub", SubscribeCreateDestroy, basename="make_sub")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"current-user", SelectedUserViewSet, basename="current_user")
router.register(r"user-subs", SubsUserViewSet, basename="user_subs")

urlpatterns += router.urls
