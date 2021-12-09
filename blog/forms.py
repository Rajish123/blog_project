from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import *

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['album', 'title', 'audio']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget = forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']