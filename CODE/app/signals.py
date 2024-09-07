# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from .models import Unattended

# @receiver(pre_delete, sender=Unattended)
# def delete_file_on_model_delete(sender, instance, **kwargs):
#     # Pass False so FileField doesn't save the model instance.
#     instance.video.delete(False)
