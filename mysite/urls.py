"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls), #' ' 빈 공간이면 naver.com/여기에 아무것도 없어도 자동으로 인식
    #path('',include("users.urls")), # 여기를 빈 공간으로 두고 애플리케이션 urls만 인식 시켜주면 이제 주소에 대한거는 해당 애플리케이션 urls에서
    path('', include("polls.urls", namespace='polls')),
    path('accounts/', include("accounts.urls", namespace='accounts')),
    path('main/', include("main.urls", namespace = 'main')),
]

