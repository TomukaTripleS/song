from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .exceptions import Conflict
from .models import Artist, Song
from .serializers import ArtistSerializer, SongSerializer


class ArtistListView(APIView):
    def get(self, request):
        return Response(ArtistSerializer(Artist.objects.all(), many=True).data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtistDetailView(APIView):
    def get(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        return Response(ArtistSerializer(artist).data)

    def patch(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        try:
            artist.delete()
        except ProtectedError:
            count = artist.songs.count()
            raise Conflict(
                f"Неможливо видалити виконавця: кількість його пісень — {count}. "
                "Спочатку видаліть ці пісні або змініть їхнього виконавця."
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SongListView(APIView):
    def get(self, request):
        songs = Song.objects.select_related("artist").all()
        return Response(SongSerializer(songs, many=True).data)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SongDetailView(APIView):
    def get(self, request, pk):
        song = get_object_or_404(Song.objects.select_related("artist"), pk=pk)
        return Response(SongSerializer(song).data)

    def patch(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        serializer = SongSerializer(song, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnknownEndpointView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        raise NotFound("Такого ендпоінта немає. Перевірте URL у README.")
