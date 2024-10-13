from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from filterings.models import Category, District

# Create your models here.

MONTHS= [
    ("january", "January"),
    ("february", "February"),
    ("march", "March"),
    ("april", "April"),
    ("may", "May"),
    ("june", "June"),
    ("july", "July"),
    ("august", "August"),
    ("september", "September"),
    ("october", "October"),
    ("november", "November"),
    ("december", "December"),
]

class PostModel(models.Model):
    title= models.CharField(max_length=100)
    bedrooms= models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    bathrooms= models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ], null= True, blank=True
    )
    balcony= models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ], null= True, blank=True
    )
    floor_number= models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],null= True, blank=True
    )
    additional_information= models.CharField(max_length=100, null=True, blank=True)
    image_url= models.URLField(max_length=512, null= True, blank=True)
    owner= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_from= models.CharField(max_length=10, choices=MONTHS)
    rent= models.DecimalField(max_digits=12, decimal_places=2)
    category= models.ManyToManyField(Category)
    district= models.ForeignKey(District, on_delete=models.CASCADE)
    area= models.CharField(max_length=100)
    on_created= models.DateTimeField(auto_now_add=True)
    on_updated= models.DateTimeField(auto_now=True)
    is_published= models.BooleanField(default=False)
    is_order= models.BooleanField(default=False)
    is_accepted= models.BooleanField(default=False)
    class Meta:
        ordering= ['-on_updated']
    def __str__(self):
        return self.title

    

REVIEWSTAR=[
    ("★","★"),
    ("★★","★★"),
    ("★★★","★★★"),
    ("★★★★","★★★★"),
    ("★★★★★","★★★★★"),
]

class ReviewModel(models.Model):
    post= models.ForeignKey(PostModel, on_delete=models.CASCADE)
    name= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment')
    user_full_name= models.CharField(max_length=100, null=True, blank=True)
    rating= models.CharField(max_length=10, choices=REVIEWSTAR, null=True, blank=True)
    body= models.TextField(max_length=300)
    created_on= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name.username



    