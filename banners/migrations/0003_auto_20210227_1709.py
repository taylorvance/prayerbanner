# Generated by Django 3.1.6 on 2021-02-27 17:09

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_banner_hide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='participants',
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='staff',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]