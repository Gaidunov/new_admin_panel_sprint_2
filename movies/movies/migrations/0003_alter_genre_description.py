# Generated by Django 4.0.4 on 2022-05-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_certificate_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
    ]
