from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from star_wars_api.views import UserProfileViewSet, LoginViewSet, PlanetViewSet

router = DefaultRouter()
router.register('users', UserProfileViewSet)
router.register('login', LoginViewSet, base_name='login')
router.register('planets', PlanetViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]