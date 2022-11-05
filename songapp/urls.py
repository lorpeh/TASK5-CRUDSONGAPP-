from django.urls import path
from .views import ArtisteApiView, ArtistedetailsApiView, SongApiView, SongdetailsApiView, lyricsApiView, LyricsdetailsApiView

urlpatterns = [
    path('artiste/', ArtisteApiView.as_view()),
    path('artiste/<int:Artiste_id>/', ArtistedetailsApiView.as_view()),
    path('songs/', SongApiView.as_view()),
    path('songs/<int:song_id>/', SongdetailsApiView.as_view()),
    path('lyrics/', lyricsApiView.as_view()),
    path ('lyrics/<int:lyrics_id>/', LyricsdetailsApiView.as_view()),

]