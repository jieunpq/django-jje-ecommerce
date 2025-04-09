from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path("admin/", admin.site.urls),
   path("", include("store.urls")), # dev_10
   path("account/", include("accounts.urls")), # dev_7
   path("cart/", include("cart.urls")), # dev_14
   path("orders/", include("orders.urls")), # dev_24
   path("payment/", include("payment.urls")), # dev_24
   ]

# dev_2
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)