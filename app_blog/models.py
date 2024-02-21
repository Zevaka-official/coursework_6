import pytils.translit
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone

from app_accounts.models import User
from utils.hash_storage import HashStorage, article_preview_images
from utils.const import MF_NULL


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=170, unique=True, null=True)
    content_text = models.TextField(max_length=2048, verbose_name='текст статьи')
    preview_image = models.ImageField(upload_to=article_preview_images, storage=HashStorage(),
                                      verbose_name='превью', **MF_NULL)
    create_date = models.DateTimeField(default=timezone.now, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='articles', **MF_NULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('app_blog:article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        max_len = self._meta.get_field('slug').max_length
        slug = pytils.translit.slugify(self.title)[:max_len]
        slug = f'{slug}_{self.pk}'
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
