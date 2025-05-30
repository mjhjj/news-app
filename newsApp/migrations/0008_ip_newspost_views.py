# Generated by Django 4.0.1 on 2022-04-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsApp", "0007_newspost_likes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="newspost",
            name="views",
            field=models.ManyToManyField(
                blank=True, related_name="post_views", to="newsApp.Ip"
            ),
        ),
    ]
