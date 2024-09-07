from app.models import Item
from django.db import models
from django.contrib.auth.models import User

class Favourites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favourites')
    items  = models.ManyToManyField(Item)

