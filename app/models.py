"""
Definition of models.
"""

from django.db import models

# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    def _str_(self):
        return self.title


    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статья блога" 
admin.site.register(Blog)

class Comment(models.Model):
        text = models.TextField(verbose_name = "Коментарий")
        date = models.TextField(default = datetime.now(), db_index = True, verbose_name = "Дата")
        author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
        post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

        def __str__(self):
            return 'Коментарий %s к %s' % (self.author, self.post)

        class Meta:
                db_table = "Comments"
                verbose_name = "Коментарий"
                verbose_name_plural = "Коментарии"
                ordering = ["-date"]
 

