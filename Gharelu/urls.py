from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html', {})

urlpatterns = [
    path('', index_view),
    path('admin/', admin.site.urls),
    path('api/products/', include('products.api.urls')),
    path('api/accounts/', include('accounts.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

