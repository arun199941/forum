from  django.db.models import  F
from .models import  UserVote,Comment
from django.dispatch import  receiver
from django.db.models.signals import  post_save,post_delete



@receiver(post_save,sender=Comment, dispatch_uid='comment_added')
def comment_added(sender,instance,**kwargs):
    created = kwargs.pop('created')
    post = instance.post

    if created:
        post.no_comment = F("no_comment") + 1
        post.save()

@receiver(post_save, sender=UserVote, dispatch_uid="user_voted")
def user_voted(sender,instance, **kwargs):
    created = kwargs.pop('created')
    content_obj = instance.content_object

    if created:
        if instance.vote_type == UserVote.UP_VOTE: 
            content_obj.change_upvote_count(1)
        else: 
            content_obj.chnage_downvote_count(1)
    else:
        if instance.vote_type == UserVote.UP_VOTE:
            content_obj.change_upvote_count(1)
            content_obj.change_downvote_count(-1)
        else:
            content_obj.change_upvote_count(-1)
            content_obj.change_downvote_count(1)

@receiver(post_delete, sender=UserVote, dispatch_uid="user_vote_deleted")
def user_vote_deleted(sender, instance, **kwargs):
    content_obj = instance.content_object
    if instance.vote_type == UserVote.UP_VOTE: 
        content_obj.change_upvote_count(-1)
    else: 
        content_obj.change_downvote_count(-1)



