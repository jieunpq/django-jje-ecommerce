from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("store.urls")), # dev_1
    path('accounts/', include('accounts.urls', namespace='accounts')),  # ✅ 이 줄이 꼭 필요!

]

# dev_2
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    