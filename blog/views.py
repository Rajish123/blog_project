from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from django.db.models import Case,When

# Create your views here.
def register(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
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
@user_passes_test(lambda u: u.is_superuser)
def add_artist(request):
    context = {}
    if request.method == "POST":
        artistform = ArtistForm(request.POST, request.FILES)
        if artistform.is_valid():
            artistform.save()
            messages.success(request, "Added successfully")
            return redirect('home')
    else:
        artistform = ArtistForm()
    context['artistform'] = artistform
    return render(request,'blog/add_artist.html',context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_album(request):
    context = {}
    if request.method == "POST":
        albumform = AlbumForm(request.POST, request.FILES)
        if albumform.is_valid():
            albumform.save()
            messages.success(request, "Added successfully")
            return redirect('home')
    else:
        albumform = AlbumForm()
    context['albumform'] = albumform
    return render(request,'blog/add_album.html',context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_song(request,album_id):
    context = {}
    album = get_object_or_404(Album,album_id =album_id)
    if request.method == "POST":
        songform = SongForm(request.POST, request.FILES)
        if songform.is_valid():
            songform.save()
            messages.success(request, "Added successfully")
            return redirect('home')
    else:
        songform = SongForm(instance=album)
    context = {'album' : album, 'songform' : songform}
    return render(request,'blog/add_song.html',context)

def artist_list(request):
    context = {}
    artistlist = Artist.objects.all()
    context['artist_list'] = artistlist
    return render(request,'blog/artist_list.html', context)

def album_list(request):
    context = {}
    allalbum = Album.objects.all()
    context['album_list'] = allalbum
    return render(request, 'blog/album_list.html', context)

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
def belonging_song(request,album_id):
    context = {}
    album = get_object_or_404(Album,album_id = album_id)
    song_list = album.song_set.all()
    context['belonging_song'] = song_list
    return render(request, 'blog/belonging_song.html', context)

@login_required
def add_to_my_playlist(request):
    if request.method == "POST":
        album_id = request.POST['albumid']
        my_playlist = MyPlaylist.objects.filter(user = request.user)
        for i in my_playlist:
            if album_id == i.album_id:
                messages.info(request,"This album is already on your playlist")
                break
        else:
            playlist = MyPlaylist(user = request.user, album_id = album_id)
            playlist.save()
            messages.success(request,"Added to my albums")
            return redirect("/blog/album_list")
    return render(request, 'blog/album_list.html')

@login_required
def my_playlist(request):
    my_playlist = MyPlaylist.objects.filter(user = request.user)        
    ids = []
    for i in my_playlist:
        ids.append(i.album_id)
    # display ablum according to the time when added
    preserved = Case(*[When(pk = pk, then = pos) for pos, pk in enumerate(ids)])
    album = Album.objects.filter(album_id__in = ids).order_by(preserved)
    return render(request, 'blog/myplaylist.html',{'myalbum':album})

@login_required
def vote(request,album_id):
    album = get_object_or_404(Album,album_id = album_id)
    album.votes += 1
    album.save()
    messages.success(request,"You liked this album.")
    return redirect('albumlist')




# necessary information doesnot show in my playlist because no relationship between myplaylist and album
# to show details of albums in myalbums page there should be link between albums and myplaylist

# possible solution
    # get album_id from my playlist
    # filter albums on the base of album_id which we get from myplaylist
    # show the albums we get in album_list page
    # album_id = request.GET['album_id']

# song form doesnt save song

    


# messages.debug
# messages.error
# messages.success
# messages.warning
# messages.info








