# Generated by Django 4.2.6 on 2023-12-04 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_likes_users_likes_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='likes',
        ),
        migrations.AddField(
            model_name='likes',
            name='post',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postlikes', to='network.posts'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='likes',
            name='users',
        ),
        migrations.AddField(
            model_name='likes',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
