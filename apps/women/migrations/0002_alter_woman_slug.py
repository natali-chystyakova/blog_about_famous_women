# Generated by Django 4.2 on 2025-01-31 19:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("women", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="woman",
            name="slug",
            field=models.SlugField(max_length=255, verbose_name="URL"),
        ),
    ]
