from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'post',
    )
    search_fields = ('text', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    list_editable = ('author',)
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)
