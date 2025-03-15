from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostView, ReviewView, SinglePostReview, ContactUsView, NewsletterView



router= DefaultRouter()
router.register("list", PostView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('review/<int:pk>/', ReviewView.as_view(), name='review_post'),
    path('reviews/<int:pk>/', SinglePostReview.as_view(), name='reviews_get'),
    path('contact-us/', ContactUsView.as_view(), name="contact-us"),
    path('newsletter/', NewsletterView.as_view(), name="newsletter")
]
