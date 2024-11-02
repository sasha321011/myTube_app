from rest_framework.routers import DefaultRouter
from clients.views import (
    SubscribeCreateDestroy,
    ProfileViewSet,
    SelectedUserViewSet,
    SubsUserViewSet,
)

urlpatterns = []

router = DefaultRouter()
router.register(r"make-sub", SubscribeCreateDestroy, basename="make_sub")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"current-user", SelectedUserViewSet, basename="current_user")
router.register(r"user-subs", SubsUserViewSet, basename="user_subs")

urlpatterns += router.urls
