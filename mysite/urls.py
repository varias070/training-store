from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('store.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', include('registration.urls')),
] + static(settings.STATIC_URL,)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
