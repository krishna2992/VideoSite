# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    
    path('', upload_metadata,name='upload_metadata'),
    path('chunk', upload_chunk, name='chunk_upload'),
    path('chunk/uploaded', get_uploaded_chunks, name='uploaded_chunk'),
]
