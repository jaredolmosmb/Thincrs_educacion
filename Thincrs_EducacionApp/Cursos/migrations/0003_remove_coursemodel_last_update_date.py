# Generated by Django 3.2.7 on 2022-01-27 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0002_coursehaswhatyouwilllearn_coursemodel_whatyouwilllearnmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemodel',
            name='last_update_date',
        ),
    ]
