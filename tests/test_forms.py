from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from collection.views import TrackForm
from collection.models import Track


class FormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Track.objects.create(
            artist = 'Би2',
            title = 'Би3',
        )
    
    def setUp(self):
        self.guest_client = Client()

    def test_create_track(self):
        tracks_count = Track.objects.count()

        form_data = {
            'title': 'трек 1',
            'artist': 'артист',
        }

        response = self.guest_client.post(
            reverse('tracks_create'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('tracks_list'))
        self.assertEqual(Track.objects.count(), tracks_count + 1)
        self.assertTrue(
            Track.objects.filter(
                artist='артист',
                title='трек 1',
            ).exists()
        )

    def test_get_track_create(self):
        tracks_count = Track.objects.count()

        form_data = {
            'title': 'трек 1',
            'artist': 'артист',
        }

        response = self.guest_client.get(
            reverse('tracks_create'),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Track.objects.count(), tracks_count)
        self.assertFalse(
            Track.objects.filter(
                title='трек 1',
            ).exists()
        )

    def test_invalid_form(self):
        tracks_count = Track.objects.count()

        form_data = {
            'title': 'трек 1',
        }

        response = self.guest_client.post(
            reverse('tracks_create'),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Track.objects.count(), tracks_count)
        self.assertFalse(
            Track.objects.filter(
                title='трек 1',
            ).exists()
        )
