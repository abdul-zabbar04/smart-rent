from django.db import models

# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=50)
    slug= models.SlugField(max_length=55)
    def __str__(self):
        return self.name

class District(models.Model):
    name= models.CharField(max_length=30, unique=True)
    slug= models.SlugField(max_length=35, unique=True, null=True, blank=True)
    class Meta:
        ordering= ['name']
    def __str__(self):
        return self.name