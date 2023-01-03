from rest_framework import routers

from theatre.views import MovieViewSet, ShowViewSet, SeatViewSet

router = routers.DefaultRouter()

router.register(r'movies', MovieViewSet, basename="movies")
router.register(r'shows', ShowViewSet, basename="shows")
router.register(r'seat', SeatViewSet, basename="seat")

urlpatterns = router.urls
