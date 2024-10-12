from django.contrib import admin

from service.models import Video, TagPost, Comment, UserVideoRelation

admin.site.register(Video)
admin.site.register(TagPost)
admin.site.register(Comment)
admin.site.register(UserVideoRelation)
