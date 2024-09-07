# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('recent', index, name='recent'),
    path('most/viewed', most_viewed, name='most_viewed'),
    path('full', full_videos, name='full_videos'),
    path('related/<uuid:uuid>/<str:name>', related, name='related'),
    path('tag/<int:pk>', tag_page, name='tag'),
    path('actor/<int:pk>', actor_page, name='actor'),
]
