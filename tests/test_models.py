from django.test import TestCase
from collection.models import Track
from users.models import Token, User


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
            'Unnamed track #10 (Unnamed Artist)'
        )

class TokenModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем ее в качестве переменной класса
        cls.user = User.objects.create(email="test")

        cls.token_value = "test-token-value"
        cls.inactive_value = "inactive-token"
        cls.invalid_token_value = "some-invalid-token"

        cls.active_token = Token.objects.create(user=cls.user, value=cls.token_value, active=True)
        cls.inactive_token = Token.objects.create(user=cls.user, value=cls.inactive_value, active=False)

    def test_token_validation(self):
        self.assertEquals(Token.validate_token(self.__class__.token_value), self.__class__.user)
        self.assertIsNone(Token.validate_token(self.__class__.invalid_token_value))

    def test_inactive_token(self):
        self.assertIsNone(Token.validate_token(self.__class__.inactive_value))