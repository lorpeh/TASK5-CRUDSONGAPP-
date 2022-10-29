from tkinter import CASCADE
from django.db import models

class Artiste(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    age = models.IntegerField()

class Song(models.Model):
    artiste = models.ForeignKey(Artiste, on_delete=models.CASCADE)
    title =models.CharField(max_length=100)
    date_released = models.DateField()
    likes = models.IntegerField()
    artist_id = models.CharField(max_length=50)

class Lyrics(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.TextField()
    song_id = models.IntegerField()

# Create your models here.
