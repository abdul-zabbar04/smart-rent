from django.db import models
from django.conf import settings
from posts.models import PostModel

class FavoriteModel(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_favorite')
    post= models.ForeignKey(PostModel, on_delete=models.CASCADE)
    post_url= models.URLField(null=True, blank=True)
    create_on= models.DateTimeField(auto_now_add=True)
    post_title= models.CharField(max_length=30, null= True, blank=True)
    def __str__(self):
        return self.post.title
    

ORDER_STATUS=[
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
]    
class OrderModel(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    owner= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    post= models.ForeignKey(PostModel, on_delete=models.CASCADE)
    ordered_time= models.DateTimeField(auto_now_add=True)
    post_title= models.CharField(max_length=100, null=True, blank=True)
    post_detail_link= models.URLField(null=True, blank=True)
    status= models.CharField(max_length=10, choices=ORDER_STATUS, default='Pending', null=True, blank=True)
    is_accepted= models.BooleanField(default=False)
    class Meta:
        ordering= ['-ordered_time']
    def __str__(self):
        return f'{self.user.username} ordered {self.post.owner.username}\'s house.'
