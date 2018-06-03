from rest_framework import viewsets, permissions, filters

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from django_filters.rest_framework.backends import DjangoFilterBackend

from star_wars_api.models import Planet, UserProfile
from star_wars_api.serializers import PlanetSerializer, UserProfileSerializer
from star_wars_api.configurations.permissions import UpdateOwnProfile


class PlanetViewSet(viewsets.ModelViewSet):
    """Handles listing, creating and updating Planets"""

    serializer_class = PlanetSerializer
    queryset = Planet.objects.all()
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )
    filter_fields = (
        'name',
        'climate',
        'terrain',
        'movie_appearances'
    )


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles listing, creating and updating Planets"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        UpdateOwnProfile,
    )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    search_fields = (
        'name',
        'email'
    )
    ordering_fields = (
        'name',
    )
    filter_fields = (
        'name',
        'email'
    )


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and return an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token"""

        return ObtainAuthToken().post(request=request)

