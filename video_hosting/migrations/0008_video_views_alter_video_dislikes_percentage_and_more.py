# Generated by Django 4.1.2 on 2022-12-01 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_hosting', '0007_remove_video_dislikes_remove_video_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=869451),
        ),
        migrations.AlterField(
            model_name='video',
            name='dislikes_percentage',
            field=models.IntegerField(default=9),
        ),
        migrations.AlterField(
            model_name='video',
            name='likes_percentage',
            field=models.IntegerField(default=81),
        ),
    ]
