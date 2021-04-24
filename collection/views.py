import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import PlayListForm, Playlist, TrackForm, Track


class TrackView(CreateView):
    form_class = TrackForm
    template_name = "new_track.html"
    success_url = reverse_lazy('tracks_list')


class TracksList(ListView):
    model = Track
    template_name = "tracks.html"

    def get_context_data(self, **kwargs):
        """Добавляем в контекст текущий день"""
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
class PlaylistList(ListView):
    model = Playlist
    template_name = "playlists.html"


@method_decorator(login_required, name='dispatch')
class PlaylistView(CreateView):
    form_class = PlayListForm
    template_name = "new_playlist.html"
    success_url = reverse_lazy('playlists_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)