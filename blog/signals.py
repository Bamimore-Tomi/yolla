from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from .models import Post, Comment

@receiver(pre_save , sender=Comment)
def update_comment_count(sender, instance, *args, **kwargs):
    """ Using this method to populate post commnets becuase comments cannot be edited.
    This method will be flawed if users can edit or update comment because each 
    save or update operation wil add 1 to the comment count which is not supposed to be."""
    instance.post.comment_count+=1
    instance.post.save()