# Generated by Django 3.1.6 on 2021-03-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210201_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='weekend',
            field=models.CharField(blank=True, max_length=100, verbose_name='participant weekend'),
        ),
    ]
