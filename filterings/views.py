from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from filterings.models import District, Category
from accounts.models import CustomUser
from posts.models import PostModel
from posts.serializers import PostSerializer
from filterings.serializers import CategorySerializer, DistrictSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class CategoryFilter(viewsets.ViewSet):
    filter_backends= [filters.OrderingFilter]
    ordering_fields = ['rent']
    def retrieve(self, request, *args, **kwargs):
        params= kwargs.get('category')
        try:
            category= Category.objects.get(slug=params)
            posts= PostModel.objects.filter(is_published=True, category=category)
            ordering = request.query_params.get('ordering', None)
            if ordering:
                posts = posts.order_by(ordering)
            # Instantiate pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Set the page size
            # Apply pagination to the queryset
            paginated_posts = paginator.paginate_queryset(posts, request)
            # serializer= PostSerializer(posts, many= True, context={'request': request})
            serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
            # return Response(serializer.data)
            return paginator.get_paginated_response(serializer.data)
        except District.DoesNotExist:
            return Response({"error": "District not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class DistrictFilter(viewsets.ViewSet):
    filter_backends= [filters.OrderingFilter]
    ordering_fields = ['rent']
    def retrieve(self, request, *args, **kwargs):
        params= kwargs.get('district')
        try:
            dis= District.objects.get(slug=params)
            posts= PostModel.objects.filter(is_published=True, district=dis)
            ordering = request.query_params.get('ordering', None)
            if ordering:
                posts = posts.order_by(ordering)
            # Instantiate pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Set the page size
            # Apply pagination to the queryset
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except District.DoesNotExist:
            return Response({"error": "District not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
class OwnerFilter(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):
        params= kwargs.get('owner')
        try:
            owner= get_object_or_404(CustomUser, username=params)
        except:
            owner= None
        try:
            posts= PostModel.objects.filter(owner=owner)
            # posts= get_object_or_404(PostModel, owner= owner)
        except PostModel.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer= PostSerializer(posts, many= True)
        return Response(serializer.data)
    
class CategoryView(viewsets.ModelViewSet):
    serializer_class= CategorySerializer
    queryset= Category.objects.all()
    permission_classes= [DjangoModelPermissionsOrAnonReadOnly]

class DistrictView(viewsets.ModelViewSet):
    serializer_class= DistrictSerializer
    queryset= District.objects.all()
    permission_classes= [DjangoModelPermissionsOrAnonReadOnly]
    