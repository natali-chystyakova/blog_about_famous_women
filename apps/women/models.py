from django.db import models
from django.urls import reverse


class Woman(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("women:post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"  # в админ панели так будет называться во множественном числе
        ordering = ["time_create", "title"]  # сортировка в админпанели


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"  # в админ панели так будет называться во множественном числе
        ordering = ["id"]  # сортировка в админпанели

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("women:category", kwargs={"cat_slug": self.slug})
