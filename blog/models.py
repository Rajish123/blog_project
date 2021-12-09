from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_picture')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (491,657)
            # resize previous image
            img.thumbnail(output_size)
            # override previous image
            img.save(self.image.path)

class Artist(models.Model):
    image = models.ImageField(default = 'default.jpg', upload_to = "artist_picture")
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    album_logo = models.ImageField(default = 'album_logo.jpg', upload_to = "album_logo_picture")
    release_date = models.DateTimeField(default=timezone.now)
    genre = models.CharField(max_length=50)
    producer = models.CharField(max_length=100)
    description = models.TextField(max_length = 250,null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.album_name

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    audio = models.FileField(upload_to = "mp3")

    def __str__(self):
        return self.title

class MyPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_id = models.CharField(max_length=10000000, default = "")







