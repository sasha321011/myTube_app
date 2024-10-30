from rest_framework.routers import DefaultRouter
from clients.views import SubscribeCreate, ProfileViewSet,Currentuser,SubsUser

urlpatterns = []

router = DefaultRouter()
router.register(r"make-sub", SubscribeCreate, basename="make_sub")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"current-user", Currentuser, basename="current_user")
router.register(r"user-subs", SubsUser, basename="user_subs")

urlpatterns += router.urls