from django.urls import path
from .views import ArtistListView, ArtistDetailView, SongListView, SongDetailView

urlpatterns = [
    path("artists/", ArtistListView.as_view()),
    path("artists/<int:pk>/", ArtistDetailView.as_view()),
    path("songs/", SongListView.as_view()),
    path("songs/<int:pk>/", SongDetailView.as_view()),
]
