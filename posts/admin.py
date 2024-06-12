from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
