# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('channels', all_channels, name='channels'),
    path('channel/home', channel_home2, name='channel_home'),
    path('actors', all_actors, name='actors'),
    path('video/<uuid:uuid>/<str:name>', viedo_item, name='video'),
    path('tag/<str:name>', get_video_by_tag, name='tag'),
    path('channel/<str:name>', get_video_by_channel, name='channel'),
    path('actor/<str:name>', get_video_by_actor, name='actor'),
    path('comments/<int:pk>', get_comments, name='comments'),
    path('post/comments/<int:pk>', post_comment, name='post_comment'),
    path('search/suggestions/<str:word>', get_search_suggestion, name='suggest_search'),
    path('search', search, name='search'),
    path('download/<str:file_name>', download_file, name='download_file'),
    path('videos/full', full_videos, name='full_videos'),
    path('videos/recent', most_recent, name='most_recent'),
    path('videos/most/viewd', most_viewed, name='most_viewed'),
]
