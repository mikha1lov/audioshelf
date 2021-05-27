from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('tracks/<int:track_id>', views.track_example, name='track_example'),

    path('tracks/', views.TracksList.as_view(), name='tracks_list'),
    path('tracks/new', views.TrackView.as_view(), name='tracks_create'),

    path('playlists/', views.PlaylistList.as_view(), name='playlists_list'),
    path('playlists/new', views.PlaylistView.as_view(), name='playlists_create'),

    path('api/tracks', api.tracks_list, name='api_tracks'),
    path('api/playlists', api.playlists_list, name='api_playlists'),
]