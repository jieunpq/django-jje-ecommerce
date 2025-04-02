from django.contrib import admin
from django.urls import path, include
from . import views

# dev_8
app_name = "store"

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"), # dev_8 about 페이지 추가
    path('product/<int:product_id>', views.product, name="product") # dev_13 제품상세페이지 추가
]
