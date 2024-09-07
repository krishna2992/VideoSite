from django.db import models
from django.contrib.auth.models import User
import uuid




class Actor(models.Model):
    name = models.CharField(max_length=100)
    ratings = models.FloatField(default=0)
    views = models.IntegerField(default=0)
    subscribers = models.ManyToManyField(User, related_name='subscribed_actors', blank=True)
    subscribers_count = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    


CHANNEL_TYPES = (
        ('channel', 'Channel'),
        ('indivisual', 'Indivisual'),
    )

class Channel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ratings = models.FloatField(default=0)
    views = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    type = models.CharField(choices=CHANNEL_TYPES, max_length=25, default='')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='channel')
    profile_picture = models.ImageField(upload_to='profiles', default='profiles/profile_image.png')
    subscribers = models.ManyToManyField(User, related_name='subscribed_channels', blank=True)
    subscribers_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return self.name
    



    


class Creator(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    views = models.IntegerField(default=0)
    actors = models.ManyToManyField(Actor)
    tags = models.ManyToManyField(Tag)
    rating = models.FloatField(default=0.0)
    duration = models.IntegerField(default=0, null=True)
    isFull = models.BooleanField(default=False)
    channel= models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    thumb = models.FileField(upload_to='thumbs', default='thumbs/output.webm')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


RESOLUTION_CHOICES= [
    ('240p', '240p'),
    ('360p', '360p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p'),
    ('4k', '4k'),
]

STATUS_CHOICES = [
    ('incomplete', 'Incomplete'),
    ('done', 'Done'),
]


class Unattended(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    actors = models.ManyToManyField(Actor)
    tags = models.ManyToManyField(Tag)
    isFull = models.BooleanField(default=False)
    channel= models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True)
    video = models.FileField(upload_to='videos', null=True)
    duration = models.IntegerField(default=0, null=True)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    orginal_resolution = models.CharField(max_length=5, choices=RESOLUTION_CHOICES, blank=True)
    thumb = models.FileField(upload_to='thumbs', null=True)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.name

class Resolution_Video(models.Model):
    resolution = models.CharField(max_length=5, choices=RESOLUTION_CHOICES)
    video = models.FileField(upload_to='videos', blank=False, null=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='resolutions', default=0, null=False)





class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replys')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-id']



from django.db.models.signals import pre_delete,post_delete
from django.dispatch import receiver
import shutil
from django.conf import settings
import os

# @receiver(pre_delete, sender=Unattended)
# def delete_file_on_model_delete(sender, instance, **kwargs):
#     # Pass False so FileField doesn't save the model instance.
#     instance.video.delete(False)

@receiver(pre_delete, sender=Item)
def delete_resolution_on_item_delete(sender, instance, **kwargs):
    resolutions = instance.resolutions.all().delete()


@receiver(pre_delete, sender=Resolution_Video)
def delete_video_on_resolution_delete(sender, instance, **kwargs):
    instance.video.delete(False)

@receiver(post_delete, sender=Unattended)
def delete_video_on_unattended_delete(sender, instance, **kwargs):
    uuid_ = instance.uuid
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
    unique_dir = os.path.join(temp_dir, str(uuid_))
    if os.path.isdir(unique_dir):
        shutil.rmtree(unique_dir)
        print(f"Directory '{unique_dir}' has been deleted.")
    else:
        print(f"Directory '{unique_dir}' does not exist.")

        