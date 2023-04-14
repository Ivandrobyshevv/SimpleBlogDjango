from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'

    title = models.CharField("Название", max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField("Описание")
    publish = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    status = models.CharField("Статус", max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="Автор")

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-publish"]

    def __str__(self):
        return self.title[:30]
