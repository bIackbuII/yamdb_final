# Generated by Django 2.2.16 on 2022-03-27 09:08

import reviews.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20220326_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.models.year_validator], verbose_name='Год выпуска'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=100, verbose_name='Роль'),
        ),
    ]
