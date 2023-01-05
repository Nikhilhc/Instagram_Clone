from django.contrib import admin

# Register your models here.
from .models import Post,Like,Follower,Comment,Hashtag,User

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Comment)
admin.site.register(Hashtag)