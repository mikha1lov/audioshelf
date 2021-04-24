from django.urls import path

from . import views

urlpatterns = [
    path('tracks', views.TracksList.as_view(), name='tracks_list'),
    path('tracks/new', views.TrackView.as_view(), name='create_track'),
]