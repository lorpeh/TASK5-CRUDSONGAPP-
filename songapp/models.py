from django.db import models

class Artiste(models.Model):
    # id = models.IntegerField(primary_key = True, auto_increment=True)
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.first_name

class Song(models.Model):
    artiste = models.ForeignKey(Artiste, on_delete=models.CASCADE, null=True)
    title =models.CharField(max_length=100)
    date_released = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField()
    # artist_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

class Lyrics(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.TextField()
    # songs_id = models.IntegerField(null=True)


    def __str__(self):
        return self.song

# Create your models here.
