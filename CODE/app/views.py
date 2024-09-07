from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Prefetch, F
from django.contrib.auth.decorators import login_required
from .models import Item, Tag, Channel, Actor, Comment, Unattended, Resolution_Video
from moviepy.editor import VideoFileClip
from Account.models import Favourites
from django.http import HttpResponse
from django.conf import settings
from .tasks import add_unattended
from api.serializers import ItemSerializer, ItemPreviewSerializer
import os, re
import json

def search(request):
    search_query  = request.GET.get('q', None)
    words = search_query.lower().split()
    print(words)
    query = Q()
    for term in words:
        query |= Q(name__icontains=term)
    tags = Tag.objects.filter(query).distinct()
    print(tags)
    items  = Item.objects.filter(tags__in=tags).annotate(match_count=Count('tags')).order_by('-match_count')
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
        page = page_number
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_images = paginator.page(1)
        page =1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recent_images = paginator.page(paginator.num_pages)
        page =paginator.num_pages
    
    context = {
        'header':f'Result for {search_query}',
        'items': recent_images,
        'num_pages':paginator.num_pages,
        'page': page
    }
    return render(request, 'index2.html', context=context)

def index(request):
    items  = Item.objects.all()
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    # paginator = Paginator(items, 10)  # Show 10 images per page
    context = {
        'header':'Top Videos',
        'type':'viewed',
        'num_pages':paginator.num_pages
    }
    return render(request, 'endpoint/index.html', context=context)



def viedo_item_comments(request, name):
    try:
        item = Item.objects.get(name=name)
    except Item.DoesNotExist:
        raise Http404('Does not Exist')
    
    items  = Item.objects.filter(tags__in=item.tags.all()).annotate(match_count=Count('tags')).order_by('-match_count')
    
    paginator = Paginator(items, 10)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_images = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recent_images = paginator.page(paginator.num_pages)

    context = {
        'item': item,
        'items': recent_images
    }
    return render(request, 'custom.html', context=context)


def viedo_item(request, uuid, name):
    print(uuid, name)
    resolution_prefetch = Prefetch('resolutions', queryset=Resolution_Video.objects.only('resolution', 'video'))
    channel_prefetch = Prefetch('channel', queryset=Channel.objects.only('name'))
    tag_prefetch = Prefetch('tags', queryset=Tag.objects.only('name'))
    actors_prefertch = Prefetch('actors', queryset=Actor.objects.only('name'))
    item = Item.objects.prefetch_related(resolution_prefetch, channel_prefetch, tag_prefetch, actors_prefertch).filter(uuid=uuid, name=name).annotate(num_comments=Count('comments'))
    if not item:
        raise Http404('Does not Exist')
    
    item.update(views=F('views') + 1)
    item = item[0]
    item.actors.all().update(views=F('views') + 1)
    if item.channel:
        item.channel.views = F('views') + 1
        item.channel.save()

    items  = Item.objects.prefetch_related(channel_prefetch).filter(tags__in=item.tags.all()).annotate(match_count=Count('tags')).order_by('-match_count')
    # items = Item.objects.all()
    
    item_paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = item_paginator.page(page_number)
        
    except PageNotAnInteger:
        
        recent_images = item_paginator.page(1)
        
    except EmptyPage:
        
        recent_images = item_paginator.page(item_paginator.num_pages)
        

    
    fav= False
    if request.user.is_authenticated:
        try:
            favourites = Favourites.objects.get(user=request.user)
            if item in favourites.items.all():
                fav = True
            else:
                fav = False
        except Favourites.DoesNotExist:
            fav = False
        
    
    comm_pages = (item.num_comments + settings.COMMENT_PAGINATOR_PAGE_SIZE -1)//(settings.COMMENT_PAGINATOR_PAGE_SIZE ) 
    srializer = json.dumps(ItemSerializer(item).data)
    items_serializer = json.dumps(ItemPreviewSerializer(recent_images, many=True).data)
    context = {
        'comm_pages':comm_pages,
        'items': recent_images,
        'num_pages':item_paginator.num_pages,
        'fav':fav,
        'serialized_data':srializer,
        'items_serializers': items_serializer,

    }
    return render(request, 'custom2.html', context=context)


def get_video_by_tag(request, name):
    try:
        tag = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return Http404('Does Not Exist')
    items = Item.objects.filter(tags=tag)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    
    context = {
        'header':tag.name+' Videos', 
        'num_pages':paginator.num_pages,
        'type':'tag',
        'uuid':tag.pk,
    }
    return render(request, 'endpoint/index.html', context=context)


def get_video_by_channel(request, name):
    try:
        channel = Channel.objects.get(name=name)
    except Channel.DoesNotExist:
        raise Http404('Does not exist')
    
    
    items = Item.objects.filter(channel=channel)
    paginator = Paginator(items, 10)  # Show 10 images per page
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
        page = page_number
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_images = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recent_images = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    isSuscribed = False
    if request.user:
        if request.user in channel.subscribers.all():
            isSuscribed = True
    
    context = {
        'channel':channel, 
        'items': recent_images,
        'suscribed':isSuscribed,
        'num_pages':paginator.num_pages,
        'page': page
    }
    return render(request, 'Channel/channel.html', context=context)



def get_video_by_actor(request, name):
    try:
        actor = Actor.objects.get(name=name)
    except Channel.DoesNotExist:
        raise Http404('Does not exist')
    
    
    items = Item.objects.filter(actors=actor)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    isSuscribed = False
    if request.user:
        if request.user in actor.subscribers.all():
            isSuscribed = True
    
    

    context = {
        'actor':actor, 
        'suscribed':isSuscribed,
        'num_pages':paginator.num_pages,
        'type':'actor',
        'uuid':actor.pk,
    }
    return render(request, 'Actor/actor-api.html', context=context)



@login_required
def channel_home(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        raise Http404('Does not Exist')
    
    items = Item.objects.filter(channel=channel)
    unattended = Unattended.objects.filter(channel=channel)
    paginator = Paginator(items, 10)  # Show 10 images per page
    unattended_page = Paginator(unattended, 10)
    page_number = request.GET.get('page')
    try:
        recent_images = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_images = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recent_images = paginator.page(paginator.num_pages)

    context = {
        'channel':channel, 
        'items': recent_images,
        'unattended': unattended_page.page(1)
    }
    return render(request, 'Channel/channel_home.html', context=context)


@login_required
def channel_home2(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        raise Http404('Does not Exist')
    
    items = Item.objects.filter(channel=channel)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    
    context = {
        'channel':channel, 
        'num_pages': paginator.num_pages,
        'page':1
    }
    return render(request, 'Channel/channel_home_api.html', context=context)





from .forms import  UnattendedFormMain, VideoForm

@login_required
def upload_item(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        raise Http404('Channel Does not Exist')
    
    if request.method == 'POST':
        form = UnattendedFormMain(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.channel = channel
            item.save()
            return redirect('app:channel_home')
        else:
            print(form.errors)
    else:
        form = UnattendedFormMain()
    return render(request, 'upload3.html', {'form': form})






def download_file(request, file_name):

    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'step_les.mp4')    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
            return response
    else:
        return HttpResponse('File not found', status=404)



######################################################################



def get_comments(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item does not exist'}, status=404)
    
    # Fetch comments with prefetch for replies
    comments = item.comments.filter(parent=None).select_related('user').prefetch_related(
        Prefetch('replys', queryset=item.comments.select_related('user').filter(parent__isnull=False))
    )
    
    # Paginate comments
    paginator = Paginator(comments, 10)  # 10 comments per page
    page_number = request.GET.get('page')
    
    try:
        page_comments = paginator.page(page_number)
    except PageNotAnInteger:
        page_comments = paginator.page(1)
    except EmptyPage:
        page_comments = paginator.page(paginator.num_pages)
    
    # Prepare JSON response
    response = []
    for comment in page_comments:
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'replys': []
        }
        for reply in comment.replys.all():
            reply_data = {
                'content': reply.content,
                'user': reply.user.username
            }
            comment_data['replys'].append(reply_data)
        
        response.append(comment_data)
    
    return JsonResponse(response, safe=False)


@login_required
def post_comment(request, pk):
    if not request.user:
        return JsonResponse({'message':'method not allowed'},status=400)
    if request.method == 'POST':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404('Does not exist')
        
        content  = request.POST.get('content')
        parent = None
        if 'parent' in request.POST:
            parent= request.POST.parent
        if not content:
            return JsonResponse({'message':'bad request'})
        
        comment = Comment(content=content, item=item, user=request.user, parent=parent)
        comment.save()
        # comments = item.comments.count()
        return JsonResponse({'content': content, 'username':request.user.username})

    return JsonResponse({'message':'method not allowed'},status=400)



def get_search_suggestion(request, word):
    tags = Tag.objects.filter(name__icontains=word)
    tags_list = list(tags.values('id', 'name'))
    actors = Actor.objects.filter(name__icontains=word)
    actors_list = list(actors.values('id', 'name'))
    channels = Channel.objects.filter(name__icontains=word)
    channel_list = list(channels.values('id', 'name'))
    res = {}
    res['tag'] = tags_list
    res['channel'] = channel_list
    res['actor'] = actors_list
    return JsonResponse(res, safe=False)



def all_channels(request):
    
    channels = Channel.objects.order_by('ratings')
    
    # Paginate comments
    paginator = Paginator(channels, 10)  # 10 comments per page
    page_number = request.GET.get('page')
    
    try:
        recent_images = paginator.page(page_number)
        page = page_number
    except PageNotAnInteger:
        recent_images = paginator.page(1)
        page = 1
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    

    context = {
        'items': recent_images,
        'head':'Channels',
        'num_pages':paginator.num_pages,
        'page': page
    }
    return render(request, 'Channel/all.html', context=context)



def all_actors(request):
    
    channels = Actor.objects.order_by('ratings')
    
    # Paginate comments
    paginator = Paginator(channels, 10)  # 10 comments per page
    page_number = request.GET.get('page')
    
    try:
        recent_images = paginator.page(page_number)
        page = page_number
    except PageNotAnInteger:
        recent_images = paginator.page(1)
        page = 1
    except EmptyPage:
        recent_images = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    

    context = {
        'items': recent_images,
        'head':'Actors',
        'num_pages':paginator.num_pages,
        'page': page
    }
    return render(request, 'Actor/all.html', context=context)



def full_videos(request):
    items = Item.objects.filter(isFull = True)
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    context = {
        'header':'Full Videos',
        'type':'full',
        'num_pages':paginator.num_pages
    }
    return render(request, 'endpoint/index.html', context=context)




def most_recent(request):
    items = Item.objects.order_by('-created_at')
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    context = {
        'header':'Recent Videos',
        'type':'recent',
        'num_pages':paginator.num_pages
    }
    return render(request, 'endpoint/index.html', context=context)


def most_viewed(request):
    items = Item.objects.order_by('-views')
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
    context = {
        'header':'Most Viewed',
        'type':'viewed',
        'num_pages':paginator.num_pages
    }
    return render(request, 'endpoint/index.html', context=context)

    