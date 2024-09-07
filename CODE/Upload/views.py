
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from app.models import  Tag, Actor, Unattended, Channel
from app.forms import VideoForm, MetaDataForm
from django.http import Http404, JsonResponse
from app.tasks import add_unattended2
from django.shortcuts import render
from django.conf import settings
import uuid, os, re

def generate_unique_uuid(session_id):
    random_component = uuid.uuid4()
    # Combine session ID and random component to create a unique UUID
    unique_uuid = f'{session_id}-{random_component}'
    return unique_uuid

def get_actors_by_name(actors):

    names_list = actors.split(',')[1:]
    res = []
    for actor in names_list:
        if not actor:
            continue
        cleaned_actor = re.sub('\s+', ' ', actor.strip())
        act, created = Actor.objects.get_or_create(name=cleaned_actor)
        res.append(act)
    return res

def get_tags_by_name(tags):

    names_list = tags.split(',')[1:]
    res = []
    for tag in names_list:
        if not tag:
            continue
        cleaned_tag = re.sub('\s+', ' ', tag.strip())
        act, created = Tag.objects.get_or_create(name=cleaned_tag)
        res.append(act)
    return res

from .presigned_url import generate_presigned_url

@login_required
@csrf_protect
def upload_metadata(request):
    try:
        channel = request.user.channel
    except ObjectDoesNotExist:
        channel = Channel(name=request.user.username, user=request.user, type='indivisual')
        channel.save()
        
    if request.method == 'POST':
        form = MetaDataForm(request.POST, request.FILES)
        if form.is_valid():
            unatt = form.save(channel=channel)
            unique_uuid = unatt.uuid
            # file_path = unatt.video.path
            try:
                dest = str(unique_uuid)+unatt.name+'.mp4'
                key = 'media/'+dest
                unatt.video = dest
                presigned_url = generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, key)
                print(presigned_url)
                unatt.save()
                return JsonResponse({'unique_uuid':unique_uuid, 'presigned_url':presigned_url}, safe=False)
            except Exception as e:
                unatt.delete()
                print(e)
                return JsonResponse({'error':'Failed'},status=400)
        else:
            print(form.errors)   
    else:
        form = VideoForm()
    
    return render(request, 'upload.html', {'form': form})



def handle_uploaded_chunk(file_chunk, unique_filename, chunk_seq):
    # Implement logic to save the file chunk with 
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
    unique_dir = os.path.join(temp_dir, unique_filename)
    if not os.path.exists(unique_dir):
        return False
    os.makedirs(unique_dir, exist_ok=True)
    with open(os.path.join(unique_dir, str(chunk_seq)), 'wb') as destination:
        for chunk in file_chunk.chunks():
            destination.write(chunk)
    with open(os.path.join(unique_dir, 'index.txt'), 'a') as index_f:
        print(chunk_seq, file=index_f)
    return True



def get_uploaded_chunk_(unique_filename):
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
    unique_dir = os.path.join(temp_dir, unique_filename)
    if not os.path.exists(unique_dir):
        return []
    
    with open(os.path.join(unique_dir, 'index.txt'), 'a') as index_f:
        lines =[int(line) for line in index_f.readlines]
    return lines
    

def get_uploaded_chunks(request):
    if request.method == 'POST':
        unique_filename = request.POST.get('file_id', None)  # Generate unique filename
        if unique_filename == None:
            return JsonResponse({'error': 'Invalid request'}, status=400)        
        uploaded_chunks = get_uploaded_chunk_(unique_filename)
        return JsonResponse(uploaded_chunks, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
        



def upload_chunk(request):
    if request.method == 'POST':
        file_chunk = request.FILES.get('file')
        unique_filename = request.POST.get('file_id')  # Generate unique filename
        chunk_num = request.POST.get('chunk_seq')
        handle_uploaded_chunk(file_chunk, unique_filename, chunk_num)
        return JsonResponse({'message':'success'},status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


    