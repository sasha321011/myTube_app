from django.contrib import admin

from service.models import Video, TagPost, Comment, UserVideoRelation, AuthorVideosList, AddAuthorListToUser

admin.site.register(Video)
admin.site.register(TagPost)
admin.site.register(Comment)
admin.site.register(UserVideoRelation)
admin.site.register(AuthorVideosList)
admin.site.register(AddAuthorListToUser)