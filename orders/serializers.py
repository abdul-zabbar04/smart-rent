from rest_framework import serializers
from orders.models import FavoriteModel, OrderModel

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model= FavoriteModel
        fields= '__all__'
        read_only_fields=['user', 'post', 'post_url', 'create_on']
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderModel
        fields= '__all__'
        read_only_fields=['user', 'owner', 'post', 'ordered_time', 'post_title', 'post_detail_link', 'status', 'is_accepted']
