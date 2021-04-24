from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm


User = get_user_model()


class Track(models.Model):
    """Отдельный музыкальный трек"""
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist']


class Playlist(models.Model):
    """Плейлист пользователя"""
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False)
    cover = models.ImageField(upload_to='covers')

    tracks = models.ManyToManyField('Track')
