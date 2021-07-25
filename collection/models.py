from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Track(models.Model):
    """Отдельный музыкальный трек"""
    title = models.CharField(
        'Назване',
        max_length=255,
        help_text="Введите  название трека"
    )
    artist = models.CharField(
        'Автор',
        max_length=255,
        help_text="Введите автора трека"
    )

    def __str__(self):
        return f"{self.title} ({self.artist}"


class Playlist(models.Model):
    """Плейлист пользователя"""
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False)
    cover = models.ImageField(upload_to='covers', blank=True)

    tracks = models.ManyToManyField('Track')
