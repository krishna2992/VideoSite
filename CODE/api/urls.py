# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('comments/<int:pk>', get_comments, name='get_comments'),
    path('channels/suscribed', get_suscribed_channels, name='suscribed_channels'),
    path('favourite/video',add_to_favorites, name='add_fav_video'),
    path('subscribe/channel/<int:pk>/<str:name>', suscribe_channel, name='channel_suscribe'),
    path('subscribe/actor/<int:pk>/<str:name>', suscribe_actor, name='actor_suscribe'),
    path('favourites',get_favourite_items, name='fav_video'),
    path('channel/listed',get_channel_listed, name='listed_video'),
    path('channel/unlisted',get_channel_unlisted, name='unlisted_video'),
    path('invalidate/upload/<uuid:uuid_>', invalidate_upload, name='invalidate_upload'),
    path('complete/upload/<uuid:uuid_>', complete_upload, name='complete_upload'),
]
