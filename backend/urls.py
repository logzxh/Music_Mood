from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Admin panel (optional, only if needed)
    # path('admin/', admin.site.urls),

    # Your app endpoints
    path('', include('core.urls')),

    # Token authentication endpoint for login
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]