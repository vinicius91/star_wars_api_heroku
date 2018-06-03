from rest_framework import serializers
from star_wars_api.models import UserProfile
from star_wars_api.models import Planet
from star_wars_api.helpers.swapi import get_planet_appearances


class UserProfileSerializer(serializers.ModelSerializer):
    """Handles the serialization of the UserProfile class"""

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email',
            'name',
            'password',
            'url',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """User creation method overwrite in order to hash the password"""

        user = UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PlanetSerializer(serializers.ModelSerializer):
    """Handles the serialization of the Planet class"""

    class Meta:
        model = Planet
        fields = (
                'id',
                'name',
                'climate',
                'terrain',
                'movie_appearances',
                'url',
        )
        extra_kwargs = {
            'movie_appearances': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        """Planet creation method overwrite in order to get the number of movie appearances"""

        movie_appearances = get_planet_appearances(validated_data['name'])
        planet = Planet(
            terrain=validated_data['terrain'],
            climate=validated_data['climate'],
            name=validated_data['name'],
            movie_appearances=movie_appearances
        )
        planet.save()

        return planet