from django.urls import include, path, re_path
from music.views import UnknownEndpointView

urlpatterns = [
    path("api/", include("music.urls")),
    re_path(r"^.*$", UnknownEndpointView.as_view()),
]
