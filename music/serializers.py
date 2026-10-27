from rest_framework import serializers
from .models import Artist, Song


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name"]


class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.name", read_only=True)

    class Meta:
        model = Song
        fields = ["id", "title", "artist", "artist_name", "genre", "listen_url", "featured_date"]

    def validate_listen_url(self, value):
        if not value.startswith(("http://", "https://")):
            raise serializers.ValidationError("Посилання має починатися з http:// або https://.")
        return value
