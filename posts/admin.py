from django.contrib import admin

from .models import Post, Comment, LikeDislike

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # use short_text instead of 'text', incase comment too long
    list_display = ("post", "commenter", "short_text", "created_at")  
    list_filter = ("commenter", "created_at")

    def short_text(self, obj):
        if len(obj.text) > 30:
            return f"{obj.text[:30]}..." # 30 chars max + ...
        else:
            return obj.text

    short_text.short_description = "Comment Summary"  # Set col header name


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", 'reaction',)
    list_filter = ('post', 'user')