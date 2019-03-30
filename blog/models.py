from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.shortcuts import reverse
from django.utils import timezone
from django.db.models import Count
import re

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор статьи')
    post_title = models.CharField(max_length=120, blank=False, null=False, verbose_name='Заголовок', help_text='Заголовок статьи')
    post_body = models.TextField(blank=False, null=False, default=None, verbose_name='Текст статьи')
    slug = AutoSlugField(populate_from='post_title', unique_with=['author__id', 'pub_date__day'], unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания статьи')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Поставьте галочку, если хотите опубликовать объявление')
    comments_open = models.BooleanField(default=True, verbose_name='Комментарии', help_text='Уберите галочку если хотите чтобы комментарии были закрыты')
    meta_title = models.CharField(max_length=140, blank=True, null=True, verbose_name='SEO заголовок')
    meta_description = models.TextField(max_length=220, blank=True, null=True, verbose_name='SEO описание')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['pub_date']

    @property
    def get_archive_query(self):
        return reversed(Post.objects.filter(is_active=True).values("pub_date__date").order_by().annotate(Count('id')))

    @property
    def get_preview_image(self):
        try:
            my_src = re.findall(r'src="(.*?)"', self.post_body)
            #? в данной регулярке, меняет режим на ленивый, вместо жадного. https://learn.javascript.ru/regexp-greedy-and-lazy
            return my_src[0]
        except:
            return None

    def get_absolute_url(self):
        return reverse('post_url', kwargs={'post_slug': self.slug})