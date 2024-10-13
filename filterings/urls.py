from django.urls import path, include
from filterings.views import DistrictFilter, OwnerFilter, CategoryFilter, CategoryView, DistrictView
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register('categories', CategoryView, basename="categories")
router.register('districts', DistrictView, basename="districts")

urlpatterns = [
    path('', include(router.urls)),
    path('district/<str:district>/', DistrictFilter.as_view({'get': 'retrieve'}), name='filter'),
    path('owner/<str:owner>/', OwnerFilter.as_view({'get': 'retrieve'}), name='owner'),
    path('category/<str:category>/', CategoryFilter.as_view({'get': 'retrieve'}), name='category'),
]


