from django.db import models
from autoslug import AutoSlugField
from django.shortcuts import reverse
# Create your models here.

class Pages(models.Model):
    page_title = models.CharField(max_length=120, blank=False, null=False, verbose_name='Заголовок', help_text='Заголовок страницы')
    page_body = models.TextField(blank=False, null=False, default=None, verbose_name='Текст страницы')
    slug = AutoSlugField(populate_from='page_title', unique_with=['pub_date__day'], unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания страницы')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Поставьте галочку, если хотите опубликовать страницу')
    meta_title = models.CharField(max_length=140, blank=True, null=True, verbose_name='SEO заголовок')
    meta_description = models.TextField(max_length=220, blank=True, null=True, verbose_name='SEO описание')

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'
        ordering = ['-pub_date']

    def __str__(self):
        return self.page_title

    def get_absolute_url(self):
        return reverse('page_url', kwargs={'page_slug': self.slug})