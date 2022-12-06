"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from clashers_gg import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("friend_finder/", views.friend_finder, name="friend_finder"),
    path("send_friend_request/", views.send_friend_request, name="send_friend_request"),
    path("get_player_info/", views.get_player_info, name="get_player_info"),
    path("get_pending_friends/", views.get_pending_friends, name="get_pending_friends"),
    path("display_friends/", views.display_friends, name="display_friends"),
    path("show_messages/", views.show_messages, name="show_messages"),
    path("send_message/", views.send_message, name="send_message"),
    path("deny_friend_request/", views.deny_friend_request, name="deny_friend_request"),
    path("accept_friend_request/", views.accept_friend_request, name="accept_friend_request"),
]
