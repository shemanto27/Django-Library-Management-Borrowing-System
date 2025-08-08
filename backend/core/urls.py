from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="Library Management API documentation, providing endpoints for managing books, authors, and categories.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.catalog.urls')),
    path('api/', include('apps.borrow.urls')),
    path('api/', include('apps.users.urls')),



    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
