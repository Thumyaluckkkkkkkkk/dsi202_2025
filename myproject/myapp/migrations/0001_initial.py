# Generated by Django 5.1.6 on 2025-05-21 14:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='trees/')),
                ('care_instructions', models.TextField(help_text='วิธีดูแลต้นไม้ เช่น รดน้ำ ใส่ปุ๋ย')),
            ],
        ),
        migrations.CreateModel(
            name='PlantingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('size_in_sq_meters', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlantingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('monthly_1', 'ปลูก 1 ต้น/เดือน'), ('yearly_10', 'ปลูก 10 ต้น/ปี')], max_length=20)),
                ('start_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TreePlanting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planted_date', models.DateField(auto_now_add=True)),
                ('planting_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.plantingarea')),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tree')),
            ],
        ),
    ]
