from django.urls import path,include
from accounts.views import UserLoginView, UserLogoutView, ChangePasswordView


urlpatterns = [
    path('api-auth/login/', UserLoginView.as_view(), name='login_api'),
    path('api-auth/logout/', UserLogoutView.as_view(), name='logout_api'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
