# Generated by Django 2.2.4 on 2021-02-18 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20210218_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='summary',
            field=models.TextField(default='new stuff'),
            preserve_default=False,
        ),
    ]
