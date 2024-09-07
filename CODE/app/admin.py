from django.contrib import admin
from .models import Item, Actor, Tag, Channel, Comment, Unattended, Resolution_Video
# Register your models here.

admin.site.register(Actor)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Unattended)
admin.site.register(Resolution_Video)
