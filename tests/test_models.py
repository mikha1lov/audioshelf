from django.test import TestCase
from collection.models import Track


class TrackModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем ее в качестве переменной класса
        cls.track = Track.objects.create(
            title='Unnamed track #10',
            artist='Unnamed Artist',
        )

    def test_labels(self):
        track = TrackModelTest.track
        fields_verbose_values = {
            'title': 'Название',
            'artist': 'Автор',
        }
        for field_name, verbose_value in fields_verbose_values.items():
            with self.subTest(field=field_name):
                self.assertEqual(
                    track._meta.get_field(field_name).verbose_name,
                    verbose_value,
                )

    def test_help_texts(self):
        track = TrackModelTest.track
        fields_help_texts = {
            'title': 'Введите название трека',
            'artist': 'Введите автора трека',
        }
        for field_name, help_text in fields_help_texts.items():
            with self.subTest(field=field_name):
                self.assertEqual(
                    track._meta.get_field(field_name).help_text,
                    help_text,
                )

    def test_str_method(self):
        track = TrackModelTest.track
        self.assertEqual(
            str(track),
            f'Unnamed track #10 (Unnamed Artist)'
        )
