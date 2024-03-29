from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 
from django.db.models import Q
from .forms import SignUpForm
import requests  
from .models import Friendship, User, Message
from datetime import datetime

def home(request):
    return render(request,"users/home.html")


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# ------------------------------------------------------
api_key = "RGAPI-348369a6-26be-4fdc-99e0-7d763d38fc8a"
# ------------------------------------------------------

def friend_finder(incoming_req):
    if incoming_req.method == "GET":
        player_name = incoming_req.GET.get("player_name")
        # API call
        api_call = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + player_name + "?api_key=" + api_key
        
        req = requests.get(
            api_call,
            params=None,
        )

        print(req.json())

        return JsonResponse(req.json())

@login_required
def send_friend_request(incoming_req):
    if incoming_req.method == "POST":
        friend1 = incoming_req.user
        friend2 = incoming_req.POST.get("friend")

        if friend2 is None:
            return HttpResponseBadRequest("Friend Request Failed To Send: friend missing from POST request")

        # convert friend2 string to user
        try:
            friend2user = User.objects.get(riot_id=friend2)
        except:
            return HttpResponseBadRequest("That Player Doesn't Have An Account On Clashers")

        # Make the friendship
        entry = Friendship(friend1=friend1, friend2=friend2user)
        entry.save() 

        return HttpResponse("Friend Request Sent Successfully")

@login_required
def get_player_info(incoming_req):
    user_riot_id = incoming_req.user.riot_id
    api_call = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + user_riot_id + "?api_key=" + api_key
    
    req = requests.get(
        api_call,
        params=None,
    )

    print(req.json())

    return JsonResponse(req.json())

@login_required
def get_pending_friends(incoming_req):
    requesting_user = incoming_req.user
    if incoming_req.method == "GET":
        try:
            all_entries = Friendship.objects.select_related().filter(friend2=requesting_user).filter(date_of_approval=None)
            return JsonResponse([x.friend1.riot_id for x in all_entries], safe=False)
        except:
            return HttpResponseBadRequest("You Don't Have Any Friends Yet") 

@login_required
def display_friends(incoming_req):
    requesting_user = incoming_req.user
    if incoming_req.method == "GET":
        all_entries = Friendship.objects.select_related() \
            .filter(Q(friend1=requesting_user) | Q(friend2=requesting_user)) \
            .exclude(date_of_approval=None)

        friend_pairs = [[x.friend1.riot_id, x.friend2.riot_id] for x in all_entries]
        friends = list(filter(lambda x: x != requesting_user.riot_id , list(set([x for l in friend_pairs for x in l]))))
        return JsonResponse(friends, safe=False)

@login_required
def show_messages(incoming_req):
    req_user = incoming_req.user
    if incoming_req.method == "GET":
        friend = incoming_req.GET.get("friend")

        # convert friend2 string to user
        try:
            other_user = User.objects.get(riot_id=friend)
        except:
            return HttpResponseBadRequest("That Player Doesn't Have An Account On Clashers")

        messages = Message.objects.select_related().filter(
            (Q(friend1=req_user) & Q(friend2=other_user)) |
            (Q(friend1=other_user) & Q(friend2=req_user))
        ).values("send_time", "message_text", "friend1__riot_id", "friend2__riot_id")

        return JsonResponse(list(messages), safe=False)

@login_required
def send_message(incoming_req):
    req_user = incoming_req.user
    if incoming_req.method == "POST":
        friend = incoming_req.POST.get("friend")
        message_text = incoming_req.POST.get("message_text")

        # convert friend2 string to user
        try:
            other_user = User.objects.get(riot_id=friend)
        except:
            return HttpResponseBadRequest("That Player Doesn't Have An Account On Clashers")

        new_message = Message(friend1=req_user, friend2=other_user, message_text=message_text, send_time=datetime.now())
        new_message.save()

        return HttpResponse("Message sent successfully")

@login_required
def accept_friend_request(incoming_req) :
    requesting_user = incoming_req.user
    if incoming_req.method == "POST":
        friend1 = incoming_req.user
        friend2 = incoming_req.POST.get("friend")

        if friend2 is None:
            return HttpResponseBadRequest("Failed: friend missing from POST request")

        # convert friend2 string to user
        try:
            friend2user = User.objects.get(riot_id=friend2)
        except:
            return HttpResponseBadRequest("That Player Doesn't Have An Account On Clashers")

        # Accept Friend Request
        try:
            entry = Friendship.objects.select_related() \
                .filter(Q(date_of_approval=None) & Q(friend1=friend2user) & Q(friend2=requesting_user))[0]
            entry.date_of_approval = datetime.now() 
            entry.save()
        except:
            return HttpResponseBadRequest("There was a problem accepting the friend request")

        return HttpResponse("Friend Request Accepted")

@login_required
def deny_friend_request(incoming_req) :
    requesting_user = incoming_req.user
    if incoming_req.method == "POST":
        friend1 = incoming_req.user
        friend2 = incoming_req.POST.get("friend")

        if friend2 is None:
            return HttpResponseBadRequest("Failed: friend missing from POST request")

        # convert friend2 string to user
        try:
            friend2user = User.objects.get(riot_id=friend2)
        except:
            return HttpResponseBadRequest("That Player Doesn't Have An Account On Clashers")

        # Deny & Delete Friend Request
        try:
            entry = Friendship.objects.select_related() \
                .filter(Q(date_of_approval=None) & Q(friend1=friend2user) & Q(friend2=requesting_user))[0]
            entry.delete()
        except:
            return HttpResponseBadRequest("There was a problem deleting the friend request")

        return HttpResponse("Friend Request Denied")

@login_required
def whoami(incoming_req):
    return HttpResponse(incoming_req.user.riot_id)
