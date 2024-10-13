from django.urls import path
from orders.views import FavoriteView, OrderView, ConfirmOrder, UserOrders, OwnerPosts, OwnerOrderedPosts, UserFavoritePostsView

urlpatterns = [
    path('favorite/<int:pk>/', FavoriteView.as_view(), name='favorite'),
    path('user/favorite/posts/', UserFavoritePostsView.as_view(), name='user_favorite_posts'),
    path('order/<int:pk>/', OrderView.as_view(), name='order'),
    path('confirm/post/<int:post_pk>/order/<int:order_pk>/', ConfirmOrder.as_view(), name='order_confirm'),
    # the first pk is from postModel and the second pk is from OrderModel
    path('user/orders/', UserOrders.as_view(), name='user_orders'),
    path('owner/posts/', OwnerPosts.as_view(), name='owner_posts'),
    path('owner/ordered_posts/', OwnerOrderedPosts.as_view(), name='ownerOrder_posts'),
]
