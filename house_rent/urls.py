from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import RegistrationApiView, ActivateAccount, UserView, UserProfileUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('filter/', include('filterings.urls')),
    path('post/', include('posts.urls')),
    path('', include('orders.urls')),
    # path("api-auth/", include("rest_framework.urls")),
    path('api/register/', RegistrationApiView.as_view(), name= 'register'),
    path('api/user/update/', UserProfileUpdateView.as_view(), name= 'update'),
    path('user/active/<uid64>/<token>/', ActivateAccount, name='activate'),
    path('user/', UserView.as_view(), name='all_user'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)