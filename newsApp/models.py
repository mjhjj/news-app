from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Comment(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    comment = models.TextField(verbose_name="Коментар")
    time = models.DateTimeField(verbose_name="Час", auto_now=True)

    def __str__(self):
        return "Коментар"


class Ip(models.Model):  # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class NewsPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(max_length=1024, verbose_name="Опис", default="")
    text = models.TextField(verbose_name="Текст посту")
    likes = models.IntegerField(verbose_name="Кількість лайків", default=0)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    views = models.ManyToManyField(
        Ip, verbose_name="Перегляди", related_name="post_views", blank=True
    )
    comments = models.ManyToManyField(
        Comment, verbose_name="Коментарі", related_name="post_comment", blank=True
    )

    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()

    def commentaries_count(self):
        return self.comments.count()


class Like(models.Model):
    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", default=0
    )
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return "Вподобання"
