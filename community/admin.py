from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Community)
admin.site.register(Comment)
admin.site.register(UserVote)
admin.site.register(CommunityPost)
