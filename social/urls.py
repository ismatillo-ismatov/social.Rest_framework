"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.authtoken import views
from users.views import CustomAuthToken
from users.views import UserCreateApiView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import health_check

schema_view = get_schema_view(
   openapi.Info(
      title="Media API",
      default_version='v1',
      description="Social.media",
      contact=openapi.Contact(email="ismatilloismatov1995@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include("api.urls")),
    path("api-auth/",include('rest_framework.urls')),
    path('api/users/',UserCreateApiView.as_view(),name='user-create'),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/token-login',CustomAuthToken.as_view(),name="token-login"),
    path('',include("chat.urls")),
    path('swagger<format>.json|.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('health/', health_check),
]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
