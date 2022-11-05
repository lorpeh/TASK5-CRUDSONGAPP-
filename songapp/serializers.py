from rest_framework import serializers
from .models import Artiste,Song, Lyrics


class ArtisteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Artiste
        fields = ["first_name", "last_name", "age"]

# class ArtistesSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Artiste
#         fields = ["id", "first_name", "last_name", "age","middle_name"]

class SongSerializers(serializers.ModelSerializer):
    artiste = ArtisteSerializers()
    class Meta:
        model = Song
        fields = ["artiste", "title", "date_released", "likes"]
        depth = 1

class LyricsSerializers(serializers.ModelSerializer):
    song = SongSerializers(many=True)
    class Meta:
        model = Lyrics
        fields = ["song", "content"]

