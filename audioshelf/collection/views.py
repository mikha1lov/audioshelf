from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import TrackForm, Track


class TrackView(CreateView):
    form_class = TrackForm
    template_name = "new_track.html"
    success_url = reverse_lazy('tracks_list')

class TracksList(ListView):
    model = Track
    template_name = "tracks.html"