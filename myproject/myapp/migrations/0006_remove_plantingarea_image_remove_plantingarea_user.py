# Generated by Django 5.1.6 on 2025-05-29 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_plantingarea_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantingarea',
            name='image',
        ),
        migrations.RemoveField(
            model_name='plantingarea',
            name='user',
        ),
    ]
