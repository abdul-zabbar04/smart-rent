from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import PostModel, ReviewModel
from posts.serializers import PostSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.permissions import IsOwnerOrReadOnly

# Create your views here.

class PostView(viewsets.ModelViewSet):
    serializer_class= PostSerializer
    permission_classes= [IsOwnerOrReadOnly & IsAuthenticatedOrReadOnly] # required custom permission where only owner of the post can put or delete and others get only

    def get_queryset(self):
        all_posts= PostModel.objects.filter(is_published=True)
        return all_posts
    
class SinglePostReview(APIView):
    serializer_class= ReviewSerializer
    def get(self, request, pk):
        print(pk)
        all_comments= ReviewModel.objects.filter(post= pk)
        serializer = ReviewSerializer(all_comments, many=True)
        return Response(serializer.data)


class ReviewView(APIView):
    serializer_class= ReviewSerializer
         
    def post(self, request, pk, format= None):
        serializer= ReviewSerializer(data= request.data)
        if serializer.is_valid():
            try:
                post= get_object_or_404(PostModel, pk=pk)
            except:
                post= None
            if post is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            user_full_name= request.user.first_name + " " + request.user.last_name
            obj=serializer.save(name= self.request.user, post= post, user_full_name= user_full_name)
            # print(obj.name.first_name, obj.name.last_name)
            # print(user_full_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    

