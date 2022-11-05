from django.shortcuts import render
from .models import Artiste, Song, Lyrics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ArtisteSerializers, SongSerializers,LyricsSerializers
from rest_framework import status
from rest_framework.parsers import JSONParser


# ARTIST FUNCTION
class ArtisteApiView(APIView):
    def get(self, request):
        artiste = Artiste.objects.all()
        artiste_url = ArtisteSerializers(artiste, many= True)
        return Response(artiste_url.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        # data = {
        #     # 'id' : request.data.get('id'),
        #     'first_name': request.data.get('first_name'),
        #     'last_name' : request.data.get('last_name'),
        #      'age' : request.data.get('age'),
        # }
        serializer = ArtisteSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistedetailsApiView(APIView):
    def get_object(self, Artiste_id):
        try:
             return Artiste.objects.get(id = Artiste_id)
        except Artiste.DoesNotExist:
            return None
    
    # Retrieve function

    def get(self, request, Artiste_id):
        Artiste_instance = self.get_object(Artiste_id)

        if not Artiste_instance:
            return Response(
                {"res":'object with Artiste id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ArtisteSerializers(Artiste_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update function

    def put(self, request, Artiste_id):
        Artiste_instance = self.get_object(Artiste_id)
        if not Artiste_instance:
            return Response(
                {"res":'object with Artiste id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "age": request.data.get('age')
            }
        serializer = ArtisteSerializers(instance=Artiste_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete function

    def delete(self, request, Artiste_id):
        Artiste_instance = self.get_object(Artiste_id)
        if not Artiste_instance:
            return Response(
                {"res": "object with Artist id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Artiste_instance.delete()
        return Response(
            {"res":"Object deleted!"},
             status=status.HTTP_200_OK
        )
       

# SONG VIEW FUNCTION

class SongApiView(APIView):
    def get(self, request):
        song = Song.objects.all()   
        serializer = SongSerializers(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SongSerializers(data=request.data)
        if serializer.is_valid():
            artiste = serializer.validated_data.pop('artiste')
            artiste_create = Artiste.objects.create(**artiste)
            song_create = Song.objects.create(**serializer.validated_data, artiste=artiste_create)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, validated_data):
    #     tracks_data = validated_data.pop('tracks')
    #     album = Album.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return album


class SongdetailsApiView(APIView):
    def get_object(self, song_id):
        try:
            return Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return None

# Retrieve Function

    def get(self, request, song_id):
        song_instance = self.get_object(song_id)
        if not song_instance:
            return Response(
                 {"res":'object with Song id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SongSerializers(song_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Update Function
    def put(self, request, song_id):
        song_instance = Song.objects.filter(id=song_id)
        if not song_instance:
            return Response(
                {"res":'object with song id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SongSerializers(data=request.data)
        if serializer.is_valid():
            artiste = serializer.validated_data.pop('artiste')
            get_artiste = Artiste.objects.filter(id=song_id).update(**artiste)
            song_instance.update(**serializer.validated_data, artiste=get_artiste )
            return Response('update successful', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete function
    def delete(self, request, song_id):
        song_instance = self.get_object(song_id)
        if not song_instance:
            return Response(
                {"res": "object with Artist id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        song_instance.delete()
        return Response(
            {"res":"Object deleted!"},
             status=status.HTTP_200_OK)

# LYRICS VIEW FUNCTION
class lyricsApiView(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        lyrics = Lyrics.objects.all()   
        serializer = SongSerializers(lyrics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LyricsSerializers(data=request.data)
        if serializer.is_valid():
            artiste = serializer.validated_data.pop('artist')
            artiste_create = Artiste.objects.create(**artiste)
            song = serializer.validated_data.pop('song')
            song_create = Song.objects.create(**serializer.validated_data, artiste=artiste_create)
            lyrics_create = Lyrics.objects.create(**serializer.validated_data, song=song_create)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request):
    #     serializer = SongSerializers(data=request.data)
    #     if serializer.is_valid():
    #         artiste = serializer.validated_data.pop('artiste')
    #         artiste_create = Artiste.objects.create(**artiste)
    #         song_create = Son g.objects.create(**serializer.validated_data, artiste=artiste_create)
    #         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LyricsdetailsApiView(APIView):
    def get_object(self, lyrics_id):
        try:
            return Song.objects.get(id=lyrics_id)
        except Song.DoesNotExist:
            return None
# Retrieve Function

    def get(self, request, lyrics_id):
        lyrics_instance = self.get_object(lyrics_id)
        if not lyrics_instance:
            return Response(
                 {"res":'object with quo id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LyricsSerializers(lyrics_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Update Function
    def put(self, request, lyrics_id):
        lyrics_instance = Lyrics.objects.filter(id=lyrics_id)
        if not lyrics_instance:
            return Response(
                {"res":'object with song id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SongSerializers(data=request.data)
        if serializer.is_valid():
            song = serializer.validated_data.pop('song')
            get_song = Song.objects.filter(id=lyrics_id).update(**song).update(**serializer.validated_data, song=get_song )
            return Response('update successful', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


              
        serializer = SongSerializers(data=request.data)
        if serializer.is_valid():
            artiste = serializer.validated_data.pop('artiste')
            get_artiste = Artiste.objects.filter(id=song_id).update(**artiste)
            song_instance.update(**serializer.validated_data, artiste=get_artiste )
            return Response('update successful', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete function
    def delete(self, request, lyrics_id):
        lyrics_instance = self.get_object(lyrics_id)
        if not lyrics_instance:
            return Response(
                {"res": "object with Artist id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        lyrics_instance.delete()
        return Response(
            {"res":"Object deleted!"},
             status=status.HTTP_200_OK)