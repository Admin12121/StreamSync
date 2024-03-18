from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.video, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("live/", views.live, name="live"),
    path("profile/", views.profile, name="profile"),
    path("upload/", views.upload, name="upload"),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
