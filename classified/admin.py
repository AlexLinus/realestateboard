from django.contrib import admin
from .models import Classified, ClassifiedImage, Complaints
# Register your models here.

class ClassifiedImagesInline(admin.TabularInline):
    model = ClassifiedImage
    extra = 1

class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ['nmb_rooms', 'flat_price', 'author', 'creation_date', 'pub_date', 'is_active', 'views', 'slug']
    list_editable = ['is_active']
    inlines = [ClassifiedImagesInline]

    class Meta:
        model = Classified

admin.site.register(Classified, ClassifiedAdmin)


class ClassifiedImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClassifiedImage._meta.fields]

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.save()

    class Meta:
        model = ClassifiedImage


admin.site.register(ClassifiedImage, ClassifiedImagesAdmin)

class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ['id', 'creation_date', 'classified']

    class Meta:
        model = Complaints
        
admin.site.register(Complaints, ComplaintsAdmin)
