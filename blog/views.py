from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict

from .forms import *

# Create your views here.
def register(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            # Profile.objects.create(user = request.user)
            messages.success(request,f"Account for {username} successfully created.")
            return redirect('login')
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request,'blog/register.html',context)

@login_required
def Profile(request):
    context = {}
    if request.method == "POST":
        user_update = UserUpdateForm(request.POST, instance=request.user)
        profile_update = ProfileUpdateForm(request.POST,
                                            request.FILES,
                                            instance = request.user.profile)
        if user_update and profile_update.is_valid():
            user_update.save()
            profile_update.save()
            messages.success(request,"Updated successfully")
            return redirect('home')
    else:
        profile_update = ProfileUpdateForm(instance = request.user)
        user_update = UserUpdateForm(instance = request.user.profile)
    context['profile_update'] = profile_update
    context['user_update'] = user_update
    return render(request, 'blog/profile.html',context)

def home(request):
    return render(request,'blog/base.html')

@login_required
def add_artist(request):
    context = {}
    if request.method == "POST":
        artistform = ArtistForm(request.POST, request.FILES)
        if artistform.is_valid():
            artistform.save()
    else:
        artistform = ArtistForm()
    context['artistform'] = artistform
    return render(request,'blog/add_artist.html',context)

@login_required
def add_album(request):
    context = {}
    if request.method == "POST":
        albumform = AlbumForm(request.POST, request.FILES)
        if albumform.is_valid():
            albumform.save()
    else:
        albumform = AlbumForm()
    context['albumform'] = albumform
    return render(request,'blog/add_album.html',context)

@login_required
def add_song(request,id):
    context = {}
    album = get_object_or_404(Album,id =id)
    if request.method == "POST":
        songform = SongForm(request.POST, request.FILES, instance=album)
        if songform.is_valid():
            songform.save()
            messages.success(request, "Added successfully")
            return redirect('home')
    else:
        songform = SongForm(instance=album)
    context['album'] = album
    context['songform'] = songform
    return render(request,'blog/add_song.html',context)

@login_required
def artist_list(request):
    context = {}
    artistlist = Artist.objects.all()
    context['artist_list'] = artistlist
    return render(request,'blog/artist_list.html', context)

@login_required
def album_list(request):
    context = {}
    allalbum = Album.objects.all()
    context['album_list'] = allalbum
    return render(request, 'blog/album_list.html', context)

@login_required 
def song_list(request):
    allsong = Song.objects.all()
    return render(request, 'blog/song_list.html', {'song_list': allsong})


@login_required 
def artist_detail(request,id):
    context = {}
    artist = get_object_or_404(Artist, id = id)
    context['artist_info'] = artist
    return render(request,'blog/artist_detail.html', context)

@login_required 
def album_detail(request, id):
    context = {}
    album = get_object_or_404(Album, id = id)
    context['album_info'] = album
    return render(request,'blog/album_detail.html',context)

@login_required 
def belonging_album(request, id):
    context = {}
    artist = get_object_or_404(Artist, id = id)
    belonging_albums = artist.album_set.all()
    context['belonging_albums'] = belonging_albums
    return render(request, 'blog/belonging_album.html',context)

@login_required 
def belonging_song(request,id):
    context = {}
    album = get_object_or_404(Album,id = id)
    song_list = album.song_set.all()
    context['belonging_song'] = song_list
    return render(request, 'blog/belonging_song.html', context)

@login_required
def my_playlist(request):
    if request.method == "POST":
        user = request.user
        album_id = request.POST['album_id']
        my_playlist = MyPlaylist.objects.filter(user = user)
        for i in my_playlist:
            if album_id == i.album_id:
                messages.info(request,"This album is already on your playlist")
                break
            else:
                playlist = MyPlaylist(user = user, album_id = album_id)
                playlist.save()
                messages.success(request,"Added to my albums")
                return redirect("/blog/album_list")
    return render(request, 'blog/myalbums.html')



    


# messages.debug
# messages.error
# messages.success
# messages.warning
# messages.info








