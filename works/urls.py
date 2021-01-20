from rest_framework.routers import DefaultRouter

from works.views import WorkViewSet


app_name = "works"

router = DefaultRouter()
router.register(r'', WorkViewSet, basename='work')

urlpatterns = router.urls
