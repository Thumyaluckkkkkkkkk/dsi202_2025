# Generated by Django 5.1.6 on 2025-05-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='tree',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
