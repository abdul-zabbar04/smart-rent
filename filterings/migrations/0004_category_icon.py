# Generated by Django 5.0.6 on 2025-03-08 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filterings', '0003_alter_district_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.URLField(blank=True, max_length=155, null=True),
        ),
    ]
