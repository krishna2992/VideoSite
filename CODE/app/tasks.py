from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Unattended, Item, Resolution_Video
from django.conf import settings
from django.core.files import File
from pathlib import Path
import shutil, random, logging  , os
from moviepy.editor import VideoFileClip
from package.create_preview import create_preview
from PIL import Image

logger = logging.getLogger(__name__)

@shared_task
def add_unattended(pk):
    try:
        unatt = Unattended.objects.get(pk=pk)
        logger.info(f"Found  {unatt.id} :{unatt.name}")
    except Unattended.DoesNotExist:
        logger.info(f"Failed to get objects for id:{pk} ")
    except Exception as e:
        logger.info(f"Failed to get objects for id:{e} ")
    return pk



def concatenate_files(base_dir ,file_list, output_file):
    chunk_size = 1024  # Adjust chunk size as needed
    with open(output_file, 'wb') as out_file:
        for file_name in file_list:
            with open(os.path.join(base_dir, str(file_name)), 'rb') as in_file:
                for chunk in iter(lambda: in_file.read(chunk_size), b''):
                    out_file.write(chunk)




@shared_task
def add_item(uuid_):
    try:
        unatt = Unattended.objects.get(uuid=uuid_)
        if not unatt.video:
            logger.info(f"No video for :{uuid_} ")
            return uuid_
        item = unatt.item
        if not item:
            logger.info(f"No item for :{uuid_}\n Creating one ")
            item = Item(name=unatt.name, duration=unatt.duration, channel=unatt.channel, isFull=unatt.isFull, profile_picture=unatt.profile_picture, thumb=unatt.thumb)
            item.save()
        

        item.tags.add(*unatt.tags.all())
        item.actors.add(*unatt.actors.all())
        item.save()
        logger.info(f"Added tags and actors")
        resolution_item = Resolution_Video(resolution=unatt.orginal_resolution, item=item, video=unatt.video)
        resolution_item.save()
        logger.info(f"Deleeting Unattended:{uuid_}\n Creating one ")
        unatt.delete()
        logger.info(f"Created item and resolution objects for ids:{item.id}, {resolution_item.id}  ")
    except Unattended.DoesNotExist:
        logger.info(f"Failed to get objects for uuid:{uuid_} ")
    return uuid_

def get_resolution_from_height(height):
    return str(height)+'p'

@shared_task
def add_unattended2(uuid_):
    try:
        unatt = Unattended.objects.get(uuid=uuid_)
        # # name = unatt.name
        # temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
        # unique_dir = os.path.join(temp_dir, str(uuid_))
        # output_file = os.path.join(unique_dir, unatt.name+str(uuid_)+'.mp4')
        # with open(os.path.join(unique_dir, 'index.txt'), 'r') as index_f:
        #     lines = [int(line) for line in index_f.readlines()]
        #     lines.sort()
        # concatenate_files(unique_dir, lines, output_file)

        # with open(output_file, 'rb') as f:
        #     django_file = File(f, name=unatt.name+str(uuid_)+'.mp4')
        #     logger.info(f"djajngo file created")
        #     unatt.video.save(Path(output_file).name, django_file,save=True)
        #     logger.info(f"saved djajngo file")

        # clip = VideoFileClip(output_file)

        # logger.info(f"getting meta data")

        # duration = clip.duration
        # original_resolution = get_resolution_from_height(clip.size[1])
        # unatt.orginal_resolution = original_resolution
        # unatt.duration = duration
        

        # if not unatt.profile_picture:
        #     frame = clip.get_frame(random.randint(1, int(duration)))
        #     new_image = Image.fromarray(frame)
        #     new_image = new_image.resize((225, 130)) 
        #     output_thumb = os.path.join(unique_dir, str(uuid_)+'.jpg')
        #     new_image.save(output_thumb)
        #     with open(output_thumb, 'rb') as profile_pic:
        #         thumb_file = File(profile_pic)
        #         unatt.profile_picture.save(Path(output_thumb).name, thumb_file, save=True)
        #         logger.info(f"saved profile_picture")
        

        # clip_output_file = os.path.join(unique_dir, unatt.name+str(uuid_)+'.webm')
        # create_preview(clip, clip_output_file)
        # with open(clip_output_file, 'rb') as clip_out:
        #     clip_file = File(clip_out)
        #     unatt.thumb.save(Path(clip_output_file).name,clip_file,save=True)
        
        # clip.close()
        # unatt.save()    
        # logger.info(f"unattended saved")
        logger.info(f"Calling add_item task")
        add_item.delay(uuid_)
    except Unattended.DoesNotExist:
        logger.info(f"Failed to get objects for id:{uuid_} ")
    except Exception as e:
        logger.info(f"Error:{e} for uuid: {uuid_}")
    return uuid_


@shared_task
def invalidate_task(uuid_):
    try:
        unatt = Unattended.objects.get(uuid=uuid_)
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
        unique_dir = os.path.join(temp_dir, str(uuid_))
        shutil.rmtree(unique_dir)
        os.removedirs(unique_dir)  
    except Unattended.DoesNotExist:
        logger.info(f"Failed to get objects for id:{uuid_} ")
    return uuid_

