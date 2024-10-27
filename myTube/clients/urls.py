from rest_framework.routers import DefaultRouter
from clients.views import SubscribeCreate

urlpatterns = [
    
]

router = DefaultRouter()
router.register(r"api/make-sub", SubscribeCreate, basename="make_sub")


urlpatterns += router.urls
