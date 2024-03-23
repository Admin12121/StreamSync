from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('password/<str:email>/', views.password, name='password'),
    path("live/", views.live, name="live"),
    path("event/", views.event, name="event"),
    path("profile/", views.profile, name="profile"),
    path("support/", views.support, name="support"),
    path("profile_update/", views.edit, name="edit"),
    path("newspost/<str:title>/", views.newspost, name="newspost"),
    path("player/<str:title>/", views.player, name="player"),
    path("upload/", views.upload, name="upload"),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
