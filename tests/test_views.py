import datetime
from http import HTTPStatus
from users.models import Token

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from collection.models import Playlist, Track

User = get_user_model()

class ViewsTest (TestCase):
    @classmethod
    def setUpClass (cls):  # !
        super().setUpClass()

        cls.user = User.objects.create_user(username = "TestUser")

        # Add some tracks to test database
        cls.tracks = [
            Track.objects.create(title = "B Monkey", artist = "Funki Porcini"),
            Track.objects.create(title = "Чудовище", artist = "АИГЕЛ"),
            Track.objects.create(title = "На север", artist = "шумные и угрожающие выходки"),
        ]
        cls.first_track = cls.tracks[0]

    def setUp (self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.__class__.user)

    def test_authorized_zone (self):
        authorized_url = reverse('playlists_list')

        response = self.guest_client.get(authorized_url)
        self.assertRedirects(response, f'/accounts/login/?next={authorized_url}')

        response = self.authorized_client.get(authorized_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_check_context (self):
        response = self.guest_client.get(reverse('tracks_list'))

        # Today key
        self.assertIn('today', response.context)
        self.assertEqual(response.context['today'], datetime.date.today())

        # Objects list
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), len(self.__class__.tracks))

        # Proper object
        first_track = response.context['object_list'][0]
        self.assertEqual(first_track.id, self.__class__.first_track.id)


class TestCollectionsAPI (TestCase):
    @classmethod
    def setUpClass (cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username = "TestUser")
        cls.user2 = User.objects.create_user(username = "TestUser2")

        cls.token_value = "login_token"
        cls.token_2_value = "token2"

        cls.token = Token.objects.create(user=cls.user, value=cls.token_value, active=True)
        cls.token2 = Token.objects.create(user=cls.user2, value=cls.token_2_value, active=True)

        # Add some tracks to test database
        cls.tracks = [
            Track.objects.create(title = "B Monkey", artist = "Funki Porcini"),
            Track.objects.create(title = "Чудовище", artist = "АИГЕЛ"),
            Track.objects.create(title = "На север", artist = "шумные и угрожающие выходки"),
        ]
        cls.first_track = cls.tracks[0]

        cls.playlist = Playlist.objects.create(owner = cls.user)
        cls.playlist.tracks.set(cls.tracks)

    def setUp (self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.__class__.user)

    def test_tracks_list(self):
        response = self.guest_client.get(reverse('api_tracks'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn('objects', data)
        self.assertEquals(len(data['objects']), len(self.__class__.tracks))
        self.assertEquals(data['objects'][0]['id'], self.__class__.tracks[0].id)

    def test_playlist_with_token(self):
        response = self.authorized_client.get(
            reverse('api_playlists'), {},
            HTTP_TOKEN=self.__class__.token_value
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn('objects', data)
        self.assertEquals(len(data['objects']), 1)
        self.assertIn('tracks', data['objects'][0])
        self.assertEquals(len(data['objects'][0]['tracks']), self.__class__.playlist.tracks.count())

    def test_playliist_response_no_token(self):
        response = self.authorized_client.get(reverse('api_playlists'))
        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        data = response.json()
        self.assertNotIn('objects', data)
        self.assertIn('error', data)

    def test_playlist_response_token_only(self):
        response = self.guest_client.get(
            reverse('api_playlists'), {},
            HTTP_TOKEN=self.__class__.token_value
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn('objects', data)
        self.assertEquals(len(data['objects']), 1)
        self.assertIn('tracks', data['objects'][0])
        self.assertEquals(len(data['objects'][0]['tracks']), self.__class__.playlist.tracks.count())
