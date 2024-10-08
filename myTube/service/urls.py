from rest_framework import routers

from service.views import VideoView

urlpatterns = [

]
router = routers.DefaultRouter()
router.register(r'api/video',VideoView)

urlpatterns += router.urls