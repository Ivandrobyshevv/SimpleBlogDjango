from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED).select_related("author")
    # def get_queryset(self):
    #     return super().get_queryset() \
    #         .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'

    title = models.CharField("Название", max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField("Описание")
    publish = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    status = models.CharField("Статус", max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="Автор")
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-publish"]

    def __str__(self):
        return self.title[:30]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    name = models.CharField("Имя", max_length=80)
    email = models.EmailField("Email")
    body = models.TextField(verbose_name="Комментарий к посту")
    created = models.DateTimeField("Создан", auto_now_add=True, db_index=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)
    active = models.BooleanField("Статус", default=True, help_text="Выберите активен / не активен пост.")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
