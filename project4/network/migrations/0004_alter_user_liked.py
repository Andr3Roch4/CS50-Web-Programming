# Generated by Django 4.2.6 on 2023-11-02 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_user_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='network.likes'),
        ),
    ]
