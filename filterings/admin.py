from django.contrib import admin
from .models import Category, District

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('name',)}
    list_display=['name', 'slug']

class DistrictAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('name',)}
    list_display=['name', 'slug']

admin.site.register(Category, CategoryAdmin)
admin.site.register(District, DistrictAdmin)
