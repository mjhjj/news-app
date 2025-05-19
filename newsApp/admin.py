from django.contrib import admin

from newsApp.models import Ip, Like, NewsPost, Comment

# Register your models here.
admin.site.register(NewsPost)
admin.site.register(Like)
admin.site.register(Ip)
admin.site.register(Comment)
