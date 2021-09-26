from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm


User = get_user_model()


class Track(models.Model):
    """Отдельный музыкальный трек"""
    title = models.CharField(
        'Название',
        max_length=255,
        help_text="Введите название трека"
    )
    artist = models.CharField(
        'Автор',
        max_length=255,
        help_text="Введите автора трека"
    )

    def __str__(self):
        return f"{self.title} ({self.artist})"


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist']


class Playlist(models.Model):
    """Плейлист пользователя"""
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False)
    cover = models.ImageField(upload_to='covers', blank=True)

    tracks = models.ManyToManyField('Track')


class PlayListForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'slug', 'cover', 'tracks']


class Review(models.Model):
    """Модель отзывов"""
    text = models.TextField(max_length=1000)