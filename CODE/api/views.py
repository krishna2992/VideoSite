from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import CommentSerializer, ChannelSerializer, ItemSerializer, UnattendedSerializer
from app.models import Item, Channel, Actor, Unattended
from Account.models import Favourites
from django.http import JsonResponse
from django.conf import settings
from app.tasks import invalidate_task, add_unattended2


@api_view(('GET',))
def get_comments(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=404)
    
    # Fetch comments with prefetch for replies
    comments = item.comments.filter(parent=None)
    
    # Paginate comments
    paginator = Paginator(comments, 10)  # 10 comments per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_comments = paginator.page(page_number)
    except PageNotAnInteger:
        page_comments = paginator.page(1)
    except EmptyPage:
        page_comments = paginator.page(paginator.num_pages)

    serializer = CommentSerializer(page_comments, many=True)
        
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suscribed_channels(request):
    channels = request.user.subscribed_channels.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    video_id = request.data.get('video_id')  # Assuming you send video_id in the request body
    try:
        item = Item.objects.get(pk=video_id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user  # Assuming user is authenticated
    try:
        favourite = Favourites.objects.get(user=user)
    except Favourites.DoesNotExist:
        favourite = Favourites(user=user)
        favourite.save()
    
    if item in favourite.items.all():
        favourite.items.remove(item)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    favourite.items.add(item)
    return Response(status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suscribe_channel(request,pk,name):
    try:
        channel = Channel.objects.get(pk=pk, name=name)
    except Channel.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.user in channel.subscribers.all():
        channel.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    channel.subscribers.add(request.user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suscribe_actor(request,pk,name):
    try:
        actor = Actor.objects.get(pk=pk, name=name)
    except Actor.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.user in actor.subscribers.all():
        actor.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    actor.subscribers.add(request.user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favourite_items(request):
    try:
        favourites = Favourites.objects.get(user=request.user)
        fav_items = favourites.items.all()
    except Favourites.DoesNotExist:
        favourites = Favourites(user=request.user)
        favourites.save()
        fav_items = favourites.items.all()
    serializer = ItemSerializer(fav_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channel_listed(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    items =  Item.objects.filter(channel=channel)
    
    # Paginate comments
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # 10 comments per page
    page_number = request.GET.get('page', 1)
    
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channel_unlisted(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    items =  Unattended.objects.filter(channel=channel)
    
    # Paginate comments
    paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # 10 comments per page
    page_number = request.GET.get('page', 1)
    
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    serializer = UnattendedSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invalidate_upload(request, uuid_):
    try:
        unatt = Unattended.objects.get(uuid=uuid_)
        invalidate_task.delay(uuid_)    
    except Unattended.DoesNotExist:
        return JsonResponse({'message':'Bad Request'}, status=400)
    return JsonResponse({'message':'Success'}, status=201)    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complete_upload(request, uuid_):
    try:
        unatt = Unattended.objects.get(uuid=uuid_)
        add_unattended2.delay(uuid_)    
    except Unattended.DoesNotExist:
        return JsonResponse({'message':'Bad Request'}, status=400)
    return JsonResponse({'message':'Success'}, status=201)    
