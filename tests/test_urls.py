from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

class URLsTest (TestCase):
    def setUp (self):  # !
        self.guest_client = Client()

    def test_valid_url_200_response (self):  # !
        pathnames_to_test = (
            'tracks_list',
            'tracks_create',
        )

        for pathname in pathnames_to_test:
            with self.subTest(pathname = pathname):  # !
                response = self.guest_client.get(reverse(pathname))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_invalid_url_404_response (self):
        response = self.guest_client.get("/some_invalid_url_we_will_never_have_in_the_project")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)