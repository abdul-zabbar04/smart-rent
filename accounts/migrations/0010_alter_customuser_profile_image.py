# Generated by Django 5.1.1 on 2024-10-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_customuser_confirm_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
