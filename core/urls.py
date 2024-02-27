from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/shop/', include('apps.shop.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/liqpay/', include('apps.liqpay.urls')),
    path('', SpectacularSwaggerView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
