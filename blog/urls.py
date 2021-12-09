from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', auth_views.LoginView.as_view(template_name = 'blog/login.html'), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'blog/logout.html'), name = 'logout'),
    path('profile', views.Profile, name = 'profile'),
    path('', views.home, name = 'home'),
    path('add_artist',views.add_artist,name='add_artist'),
    path('add_album',views.add_album, name = "add_album"),
    path('add_song/<str:id>', views.add_song, name = "add_song"),
    path("artist_list", views.artist_list, name = "artistlist"),
    path('album_list', views.album_list, name = "albumlist"),
    path('song_list', views.song_list, name = "songlist"),
    path("artist_detail/<str:id>", views.artist_detail, name = "artistdetail"),
    path('album_detail/<str:id>', views.album_detail, name = 'albumdetail'),
    path('artist/album/<str:id>', views.belonging_album, name = 'artist_album'),
    path('album/song/<str:id>', views.belonging_song, name = 'album_song'),
    path("myplaylist", views.my_playlist, name = "my_playlist" )

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



