from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer, ChangePasswordSerializer
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated



def EmailSend(user, user2, subject, message_tem):
    message = render_to_string(message_tem, {
        'user': user,
        'user2': user2,
    })
    send_mail= EmailMultiAlternatives(subject, '', to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()

    
class UserView(APIView):
    serializer_class= UserSerializer
    permission_classes=[IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class RegistrationApiView(APIView):
    serializer_class= UserSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data= request.data)

        if serializer.is_valid():
            user= serializer.save()
            token= default_token_generator.make_token(user)
            uid= urlsafe_base64_encode(force_bytes(user.pk))   # uid full form unique id, variable; create a unique id
            print(uid)
            print("this is token",token)
            confirm_link= f"http://127.0.0.1:8000/user/active/{uid}/{token}" # Created this confirm unquie id for a user to verify him/her.
            email_subject= "Confirm Your Email"
            email_body= render_to_string('accounts/confirm_mail.html', {'confirm_link':confirm_link})
            email= EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
def ActivateAccount(request, uid64, token):
    try:
        uid= urlsafe_base64_decode(uid64).decode()
        user= CustomUser._default_manager.get(pk= uid)
    except(CustomUser.DoesNotExist):
        user= None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active= True
        user.save()
        return redirect('http://127.0.0.1:5500/frontend/login.html')
    return redirect('register')

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can update their profile
    serializer_class = UserSerializer

    def patch(self, request):
        user = request.user  # Get the currently authenticated user
        serializer = self.serializer_class(user, data=request.data, partial=True)  # partial=True allows updating specific fields

        if serializer.is_valid():
            serializer.save()  # Save the updated fields (first_name, last_name, profile_image)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)

class UserLoginView(APIView):
    serializer_class= UserLoginSerializer
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class UserLogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class= UserLoginSerializer
    def get(self, request):
        print(request.user)
        request.user.auth_token.delete()
        logout(request)
        return Response({'logout' : "Success"})
        # return redirect('http://127.0.0.1:8000/account/api-auth/login/')


class ChangePasswordView(APIView):
    serializer_class= ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)