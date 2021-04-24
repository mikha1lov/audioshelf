from django.urls import path

from . import views

urlpatterns = [
    path('tracks/', views.TracksList.as_view(), name='tracks_list'),
    path('tracks/new', views.TrackView.as_view(), name='tracks_create'),

    path('playlists/', views.PlaylistList.as_view(), name='playlists_list'),
    path('playlists/new', views.PlaylistView.as_view(), name='playlists_create'),
]