from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post
# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ['post_title', 'slug', 'is_active', 'comments_open', 'creation_date', 'author']
    summernote_fields = ('post_body',)

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)