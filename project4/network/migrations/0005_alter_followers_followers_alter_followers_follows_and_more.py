# Generated by Django 4.2.6 on 2023-12-04 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_posts_likes_likes_post_alter_likes_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followers',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followers',
            name='follows',
            field=models.ManyToManyField(blank=True, null=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followers',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
