from django.contrib import admin
from .models import PostModel, ReviewModel, ContactUs
class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'owner', 'available_from', 'on_created', 'is_published']

admin.site.register(PostModel, PostAdmin)
admin.site.register(ReviewModel)
admin.site.register(ContactUs)
