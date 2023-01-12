from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Post,Like,Follower,Comment,Hashtag,User

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, MyUserAdmin)
# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Comment)
admin.site.register(Hashtag)