# Generated by Django 3.2.3 on 2021-06-08 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotupdate', '0009_packageversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
        migrations.AddField(
            model_name='packageversion',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Note'),
        ),
    ]
