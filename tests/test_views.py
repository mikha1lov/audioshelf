from http import HTTPStatus
from django.contrib import auth

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()

class ViewsTest (TestCase):
    @classmethod
    def setUpClass (cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username = "TestUser")

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