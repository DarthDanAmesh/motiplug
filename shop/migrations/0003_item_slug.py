# Generated by Django 2.2.6 on 2019-11-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191125_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
