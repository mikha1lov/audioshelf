from django.forms import ModelForm

from .models import Track, Playlist


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist']


class PlayListForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'slug', 'cover', 'tracks']
