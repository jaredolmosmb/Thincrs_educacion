# Generated by Django 4.0.1 on 2022-02-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='category',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='description',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='language',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='locale_description',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='name',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='primary_category',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='required_education',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='requirements',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='title',
            field=models.CharField(max_length=2000),
        ),
    ]