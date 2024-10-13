# Generated by Django 5.1.1 on 2024-09-19 09:16

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filterings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('bedrooms', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('bathrooms', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('balcony', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('floor_number', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('additional_information', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('available_from', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=10)),
                ('rent', models.DecimalField(decimal_places=2, max_digits=12)),
                ('area', models.CharField(max_length=100)),
                ('on_created', models.DateTimeField(auto_now_add=True)),
                ('on_updated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(to='filterings.category')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filterings.district')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]