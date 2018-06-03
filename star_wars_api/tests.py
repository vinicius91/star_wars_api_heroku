from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from star_wars_api.models import UserProfile, Planet
from star_wars_api.helpers.swapi import get_planet_appearances


class UserProfileTest(TestCase):

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = UserProfile.objects.create_user('test@example.com', 'testuser', 'testpassword')

    def test_verify_number_of_created_users(self):
        # We want to make sure we have two users in the database..
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_verify_user_data(self):
        """Ensure that the user is created properly"""
        data = {
            'email': 'foobar@example.com',
            'name': 'foobar',
            'password': 'somepassword'
        }
        response = self.client.post('/users/', data, format='json')
        # We want to make sure we have two users in the database..
        self.assertEqual(UserProfile.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_user_login(self):
        """Verify if user can login"""
        data = {
            'username': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/login/', data, format='json')
        self.assertTrue('token' in response.data)


class PlanetTest(TestCase):

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = UserProfile.objects.create_user('planet@example.com', 'planetuser', 'planetpassword')

    def test_cant_crete_planet_anon(self):
        """Ensure that the user is created properly"""
        data = {
            'name': 'Alderaan',
            'climate': 'temperate',
            'terrain': 'grasslands, mountains'
        }
        response = self.client.post('/planets/', data, format='json')
        # We want to make sure we have no planet in the database..
        self.assertEqual(Planet.objects.count(), 0)
        # And that we're returning a 401.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Checking if the message is user friendly.
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_can_create_planet_logged(self):
        """Ensure that the user is created properly"""
        login_data = {
            'username': 'planet@example.com',
            'password': 'planetpassword'
        }
        login_response = self.client.post('/login/', login_data, format='json')
        # Getting the logged token
        token = 'Token ' + login_response.data['token']
        data = {
            'name': 'Alderaan',
            'climate': 'temperate',
            'terrain': 'grasslands, mountains'
        }
        client = APIClient()
        # Using the planet User
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.post(
            '/planets/',
            data,
            format='json',
            headers={
                'Content-Type': 'application/json'
            }
        )
        # We want to make sure we have no planet in the database..
        self.assertEqual(Planet.objects.count(), 1)
        # And that we're returning a 401.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking if all the parameters were returned
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['climate'], data['climate'])
        self.assertEqual(response.data['terrain'], data['terrain'])
        self.assertTrue('movie_appearances' in response.data)
        self.assertTrue('url' in response.data)

    def test_cant_create_planet_with_same_name(self):
        """Ensure that the user is created properly"""
        login_data = {
            'username': 'planet@example.com',
            'password': 'planetpassword'
        }
        login_response = self.client.post('/login/', login_data, format='json')
        # Getting the logged token
        token = 'Token ' + login_response.data['token']
        data = {
            'name': 'Alderaan',
            'climate': 'temperate',
            'terrain': 'grasslands, mountains'
        }
        client = APIClient()
        # Using the planet User
        client.credentials(HTTP_AUTHORIZATION=token)
        first_response = client.post(
            '/planets/',
            data,
            format='json',
            headers={
                'Content-Type': 'application/json'
            }
        )
        # We want to make sure we have no planet in the database..
        self.assertEqual(Planet.objects.count(), 1)
        # And that we're returning a 201.
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        # Posting the same planet
        second_response = client.post(
            '/planets/',
            data,
            format='json',
            headers={
                'Content-Type': 'application/json'
            }
        )
        # Count if we still have only one planet in the database
        self.assertEqual(Planet.objects.count(), 1)
        # Check if the response is a bad request 400
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

class SwapiMovieAppearancesTest(TestCase):

    def test_check_alderaan_count(self):
        """First Test case to Check an normal name"""
        alderaan = get_planet_appearances('Alderaan')
        self.assertEqual(alderaan, 2)

    def test_check_polis_massa_count(self):
        """Check a name with a space between it"""
        polis_massa = get_planet_appearances('Polis Massa')
        self.assertEqual(polis_massa, 1)
        
    def test_check_invalid_planet_count(self):
        """Check a name with a space between it"""
        invalid = get_planet_appearances('Lorem Ipsum')
        self.assertEqual(invalid, 0)
