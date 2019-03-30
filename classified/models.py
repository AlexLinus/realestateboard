from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.shortcuts import reverse

# Create your models here.
FLAT_TYPE = (('Студия', 'Студия'), ('1 комн.', '1 комн.'), ('2 комн.', '2 комн.'), ('3 комн.', '3 комн.'), ('4 комн.', '4 комн.'))

#Функция по какому принципу мы будем генерировать слаг.
def generate_slug(instance):
    return r'%s-%s-%s-%s'%(instance.author.id, instance.nmb_rooms, instance.flat_square, instance.flat_floor)

class Classified(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classifieds', verbose_name='Автор')
    nmb_rooms = models.CharField(choices=FLAT_TYPE, max_length=9, blank=False, null=False, verbose_name='Количество комнат')
    flat_square = models.PositiveIntegerField(default=1, blank=True, null=True, verbose_name='Площадь', help_text='Площадь указывается в квадратных метрах (м2)')
    flat_floor = models.PositiveIntegerField(blank=False, null=False, verbose_name='Этаж', help_text='Укажите этаж на котором расположена квартира')
    total_floor = models.PositiveIntegerField(blank=False, null=False, verbose_name='Всего этажей в доме', help_text='Укажите сколько всего этажей в доме')
    flat_price = models.PositiveIntegerField(blank=False, null=False, verbose_name='Цена', help_text='Укажите полную стоимость вашей квартиры')
    flat_description = models.TextField(max_length=2500, verbose_name='Описание', help_text='Добавьте описание квартиры. Всё то что важно знать покупателю, каковы преимущества, что выделяет вашу квартиру в сравнении с другими')
    author_phone = models.CharField(max_length=22, default=None, blank=False, null=False, verbose_name='Телефон', help_text='Введите ваш телефон, чтобы покупатель мог связаться с вами')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания объявления')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата последней публикации')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name='Просмотры', help_text='Количество просмотров вашего объявления')
    slug = AutoSlugField(default=None, null=False, blank=False, populate_from=generate_slug, unique_with=['author__id', 'pub_date__month', 'pub_date__day'], unique=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('flat_detail_url', kwargs={'flat_slug': self.slug})

    @property
    def get_price_per_meter(self):
        if self.flat_square:
            return int(self.flat_price // self.flat_square)
        else:
            return self.flat_price

    def __str__(self):
        return str(self.id)

def user_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'classifieds/uploads/user_{0}/{1}'.format(instance.author.id, filename)


class ClassifiedImage(models.Model):
    image = models.ImageField(upload_to=user_upload_directory_path, verbose_name='Изображение')
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='classified_images')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания изображения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, default=None, on_delete=models.CASCADE, related_name='user_classified_images', verbose_name='Автор (user)')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-creation_date']

    @property
    def get_src(self):
        return '/media/' + str(self.image)

    def __str__(self):
        return 'id: {0} - date: {1}'.format(self.id, self.creation_date)


class Complaints(models.Model):
    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
        ordering = ['-creation_date']

    complaint_body = models.TextField(verbose_name='Суть жалобы')
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='complaints')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания изображения')
