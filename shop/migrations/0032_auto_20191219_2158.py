# Generated by Django 2.2.6 on 2019-12-19 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20191219_2138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quantity',
            new_name='number',
        ),
    ]