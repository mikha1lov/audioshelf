from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Track(models.Model):
    """Отдельный музыкальный трек"""
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)


class Playlist(models.Model):
    """Плейлист пользователя"""
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='covers')

    tracks = models.ManyToManyField('Track')
