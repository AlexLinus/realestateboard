from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Pages
# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ['page_title', 'slug', 'is_active', 'creation_date']
    summernote_fields = ('page_body',)

    class Meta:
        model = Pages

admin.site.register(Pages, PostAdmin)