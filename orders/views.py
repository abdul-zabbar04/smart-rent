from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from orders.serializers import FavoriteSerializer, OrderSerializer
from posts.models import PostModel
from posts.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib import messages
from orders.models import OrderModel, FavoriteModel
from accounts.views import EmailSend

# Create your views here.
class FavoriteView(APIView):
    serializer_class= FavoriteSerializer   
    def post(self, request, pk, format= None):
        serializer= FavoriteSerializer(data= request.data)
        if serializer.is_valid():
            try:
                post= get_object_or_404(PostModel, pk=pk)
                print(post, "favorite post")
                post_url= f'https://smart-rent-web.netlify.app/post_detail.html?id={pk}'
                print(post_url)
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer.save(user= self.request.user, post_title= post.title, post= post, post_url= post_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def delete(self, request, pk, format=None):
    #     try:
    #         print(pk, 'this is the targeted pk')
    #         x=get_object_or_404(FavoriteModel, post_id=pk)
    #         print(x, 'this is the targeted post')
    #     except:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(status=status.HTTP_200_OK)

class UserFavoritePostsView(APIView):
    serializer_class= FavoriteSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        print(request.user.username)
        userFavoritePost= FavoriteModel.objects.filter(user= request.user.pk)
        serializer = FavoriteSerializer(userFavoritePost, many=True)
        return Response(serializer.data)


class OrderView(APIView):
    serializer_class= OrderSerializer     
    def post(self, request, pk, format= None):
        serializer= OrderSerializer(data= request.data)
        if serializer.is_valid():
            try:
                post= get_object_or_404(PostModel, pk=pk)
                if post.is_order and post.is_accepted:
                    return Response({"error": "This post is already accepted and unavailable for new requests."}, status=status.HTTP_400_BAD_REQUEST)
                post.is_order= True
                post.save()
                post_url= f'https://smart-rent-web.netlify.app/post_detail.html?id={pk}'
                # print(post_url, "this from the OrderView")
                EmailSend(request.user, post.owner, 'Thanks for Rent Request.', 'orders/user_mail.html')
                EmailSend(post.owner, request.user, 'You Received a Rent Request', 'orders/owner_mail.html')
            except:            
                return Response(status=status.HTTP_204_NO_CONTENT)
            # print(post.title, "this also from the oderView")
            serializer.save(user= self.request.user, owner=post.owner, post= post, post_title= post.title, post_detail_link= post_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserOrders(APIView):
    serializer_class= OrderSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        print(request.user.username)
        userOrderedPost= OrderModel.objects.filter(user= request.user.pk)
        print(userOrderedPost)
        serializer = OrderSerializer(userOrderedPost, many=True)
        return Response(serializer.data)
    
class OwnerPosts(APIView):
    def get(self, request):
        print(request.user.username)
        ownerPosts= PostModel.objects.filter(owner= request.user.pk)
        serializer = PostSerializer(ownerPosts, many=True, context={'request': request})
        return Response(serializer.data)
    
class OwnerOrderedPosts(APIView):
    def get(self, request):
        print(request.user.username)
        ownerOrderedPosts= OrderModel.objects.filter(owner= request.user.pk)
        serializer = OrderSerializer(ownerOrderedPosts, many=True)
        return Response(serializer.data)

class ConfirmOrder(APIView):
    serializer_class= OrderSerializer
    def post(self, request, post_pk, order_pk):
        print(post_pk, order_pk, "this is the pks")
        try:
            post = get_object_or_404(PostModel, pk=post_pk)
            order = get_object_or_404(OrderModel, pk=order_pk, post=post)
        except (PostModel.DoesNotExist, OrderModel.DoesNotExist):
            post, order = None, None

        if post and order and request.user.is_authenticated and post.is_order:
            if request.user == post.owner:
                if not post.is_accepted:
                    # In the PostModel
                    post.is_accepted = True
                    post.save()
                    # sent mail to user(1st) and owner(2nd)
                    EmailSend(order.user, post.owner, 'Confirmed Your Rent Request', 'orders/user_confirmation_mail.html')
                    EmailSend(post.owner, order.user, 'Confirmed Successfully', 'orders/owner_success_mail.html')
                    
                    # In the OrderModel
                    order.status = 'Accepted'
                    order.is_accepted = True
                    order.save()

                    # Reject all other pending orders for this post
                    other_orders = OrderModel.objects.filter(post=post, status='Pending').exclude(id=order.id)
                    other_orders.update(status='Rejected')
                    return Response({'success': "Rent request accepted. Other requests rejected."}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'error': 'Already Accepted!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not the owner of this property.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request Failed!'}, status=status.HTTP_400_BAD_REQUEST)

