import datetime
from http import HTTPStatus

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from collection.models import Track

User = get_user_model()

class ViewsTest (TestCase):
    @classmethod
    def setUpClass (cls):  # !
        super().setUpClass()

        cls.user = User.objects.create_user(username = "TestUser")

        # Add some tracks to test database
        Track.objects.create(title = "B Monkey", artist = "Funki Porcini")
        Track.objects.create(title = "Чудовище", artist = "АИГЕЛ")
        Track.objects.create(title = "На север", artist = "шумные и угрожающие выходки")

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

        self.assertIn('today', response.context)
        self.assertIsInstance(response.context['today'], datetime.date)
        self.assertEqual(response.context['today'], datetime.date.today())