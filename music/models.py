from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name="songs")
    genre = models.CharField(max_length=100)
    listen_url = models.URLField(max_length=500)
    featured_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
