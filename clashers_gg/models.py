from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    riot_id = models.CharField(max_length=32)

class Friendship(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend1")
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend2")
    date_of_approval = models.DateTimeField(null=True)

class Message(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend1_message")
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend2_message")
    send_time = models.DateTimeField()
    message_text = models.TextField()
