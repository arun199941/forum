from django.db import models
import uuid
from django.db.models import F
from  django.conf import  settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class ModelBase(models.Model):
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created= models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta():
        abstract =True

    @classmethod
    def get_or_not(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None

class Community(ModelBase):

    name =  models.TextField(max_length=100,default='')
    posts = models.ManyToManyField('Post', related_name="community", blank=True, through="CommunityPost")
    description = models.TextField(default='')
    cover_image_url = models.URLField('Cover Image URL', max_length=200, blank=True, null=True)
    captains = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="Community_captains")
    def __str__(self):
        return  self.name

class CommunityPost(ModelBase):
    community = models.ForeignKey('Community', related_name="posts_set", on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name="community_set", on_delete=models.CASCADE)

    class Meta():
        unique_together = ['community', 'post']






class Vote(ModelBase):
    upvote = models.PositiveIntegerField(default=0)
    downvote = models.PositiveIntegerField(default=0)
    class Meta: abstract = True
    @staticmethod
   
    def get_object(eid):
        post = Post.get_or_not(eid=eid)
        if post: return post
        comment = Comment.get_or_not(eid=eid)
        if comment: return comment

    def get_rank(self):
        return self.upvote - self.downvote
    
   
    def toggle_vote(self, voter , vote_type):

        uv = UserVote.get_or_not(voter=voter, object_id=self.eid)
        if uv:
            if uv.vote_type == vote_type:
                uv.delete()
            else:
                uv.vote_type = vote_type
                uv.save()
        else:
            UserVote.objects.create(voter=voter,content_object=self, vote_type=vote_type)
    
    def change_vote_count(self , vote_type, delta):
        self.refresh_from_db()
        if vote_type == UserVote.UP_VOTE:
            self.upvote = F('upvote') + delta
        elif vote_type == UserVote.DOWN_VOTE:
            self.downvote = F('downvote') + delta
        self.save()
    
    def change_upvote_count(self,delta):
        self.change_vote_count(UserVote.UP_VOTE,delta)
    def change_downvote_count(self,delta):
        self.change_vote_count(UserVote.DOWN_VOTE,delta)
    def get_user_vote(self,user):
        if not user or not user.is_authenticated: return None

        uv = UserVote.get_or_not(voter=user, object_id=self.eid)
        if not uv: 
            return None
        if uv.vote_type == UserVote.UP_VOTE: 
            return 1
        else: 
            return -1


class Post(Vote):
    title = models.CharField(max_length=200)
    submit_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts_submitted", on_delete= models.CASCADE)
    url = models.URLField('URL', max_length=200, null=True, blank= True)
    description = models.TextField(blank=True, null=True)
    no_comment = models.PositiveIntegerField(default=0)
    def children(self):
        return self.comments.filter(parent=None)

    def __str__(self):
        return str(self.eid) + ":" + self.title





class Comment(Vote):
    post = models.ForeignKey(Post, related_name="comments", on_delete= models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', related_name="children", null=True, blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.eid) + ":" + self.comment

class UserVote(ModelBase):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    VOTE_TYPE = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote')
    )

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    vote_type = models.CharField(max_length=1, choices=VOTE_TYPE)

    class Meta:
        unique_together= ['voter', 'object_id', 'content_type']


