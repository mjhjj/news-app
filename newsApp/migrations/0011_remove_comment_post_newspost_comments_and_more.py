# Generated by Django 4.0.1 on 2022-04-23 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsApp", "0010_like_post_like_reporter_remove_newspost_likes_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="post",
        ),
        migrations.AddField(
            model_name="newspost",
            name="comments",
            field=models.ManyToManyField(
                blank=True,
                related_name="post_views",
                to="newsApp.Comment",
                verbose_name="Коментарі",
            ),
        ),
        migrations.AlterField(
            model_name="newspost",
            name="views",
            field=models.ManyToManyField(
                blank=True,
                related_name="post_views",
                to="newsApp.Ip",
                verbose_name="Перегляди",
            ),
        ),
    ]
