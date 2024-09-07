from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.serializers import *
from app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.conf import settings



@api_view(('GET',))
def index(request):
    items = Item.objects.order_by('-created_at')
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
        
    except PageNotAnInteger:
        
        recent_images = paginator.page(1)
        
    except EmptyPage:
        
        recent_images = paginator.page(paginator.num_pages)
        

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)



@api_view(('GET',))
def most_viewed(request):
    items = Item.objects.order_by('-views')
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)   # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
        
    except PageNotAnInteger:
        
        recent_images = paginator.page(1)
        
    except EmptyPage:
        
        recent_images = paginator.page(paginator.num_pages)
        

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)



@api_view(('GET',))
def full_videos(request):
    items = Item.objects.filter(isFull=True)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        recent_images = paginator.page(1)
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)



@api_view(('GET',))
def related(request, uuid, name):
    item = Item.objects.filter(uuid=uuid, name=name)
    if not item:
        return Response(status=400)
    
    items  = Item.objects.filter(tags__in=item[0].tags.all()).annotate(match_count=Count('tags')).order_by('-match_count')
    items = Item.objects.all()
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        recent_images = paginator.page(1)
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)



@api_view(('GET',))
def tag_page(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except ObjectDoesNotExist:
        
        return Response(status=400)
    
    items  = Item.objects.filter(tags=tag)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        recent_images = paginator.page(1)
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)

@api_view(('GET',))
def actor_page(request, pk):
    try:
        actor = Actor.objects.get(pk=pk)
    except ObjectDoesNotExist:
        
        return Response(status=400)
    
    items  = Item.objects.filter(actors=actor)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        recent_images = paginator.page(1)
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(recent_images, many=True)
    return Response(serializer.data)