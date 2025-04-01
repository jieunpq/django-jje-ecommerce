from django.urls import path
from . import views

app_name = 'accounts'  # 이 줄을 꼭 넣어야 namespace가 작동함

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
