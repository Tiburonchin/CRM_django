"""
URL configuration for crm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from clients.views import ClientViewSet
from activities.views import ActivityViewSet
from users.views import home_view

# --- Spectacular / Docs ---
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)


# HU 6: Endpoint raíz de la API
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, version=None, *args, **kwargs):
    """
    Endpoint raíz de la API - Estado del sistema
    """
    return Response({
        'message': 'Bienvenido al API del CRM',
        'version': '1.0',
        'endpoints': {
            'clients': '/api/v1/clients/',
            'activities': '/api/v1/activities/',
            'statistics': '/api/v1/activities/statistics/',
        }
    })


# Router para DRF
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'activities', ActivityViewSet, basename='activity')

# Group API URLs so we can include them under /api/v1/
api_urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),

    # Documentation endpoints (Spectacular)
    path('schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[AllowAny]), name='redoc'),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', home_view, name='home'),

    # Versioned API (URLPathVersioning expects a version component)
    re_path(r'^api/(?P<version>(v1))/', include(api_urlpatterns)),

    # Apps
    path('users/', include('users.urls')),
    path('clients/', include('clients.urls')),
    path('activities/', include('activities.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
