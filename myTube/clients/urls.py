from rest_framework.routers import DefaultRouter
from clients.views import (
    SubscribeCreateDestroy,
    ProfileViewSet,
    SelectedUserViewSet,
    SubsUserViewSet,
)
from django.urls import path, include


profile_detail = ProfileViewSet.as_view({
    'get': 'list',    # 
    'put': 'update',  
})

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),

    path('user-profile/', profile_detail, name='user-profile'),
]

router = DefaultRouter()
router.register(r"make-sub", SubscribeCreateDestroy, basename="make_sub")
#router.register(r"user-profile", ProfileViewSet, basename="user-profile")
router.register(r"current-user", SelectedUserViewSet, basename="current_user")
router.register(r"user-subs", SubsUserViewSet, basename="user_subs")

urlpatterns += router.urls
