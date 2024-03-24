from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.video, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("live/", views.live, name="live"),
    path("profile/", views.profile, name="profile"),
    path("trending/", views.trending, name="trending"),
    path("upload/", views.upload, name="upload"),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path("event/", views.event, name="event"),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('password/<str:email>/', views.password, name='password'),
    path("profile_update/", views.edit, name="edit"),
    path("newspost/<str:title>/", views.newspost, name="newspost"),
    path("player/<str:title>/", views.player, name="player"),

]
