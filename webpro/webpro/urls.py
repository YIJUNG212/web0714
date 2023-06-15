"""
URL configuration for webpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("base",views.base),
    path("css_index",views.css_index),
    path("index",views.index),
    path("api/vip",views.vip),
    path("api/vip_register",views.vip_register),
    path("api/vip_user_add",views.vip_user_add),
    path("webuser_showfield",views.webuser_showfield),
    path("webuser_get_all",views.webuser_get_all),
    path("webuser_admin",views.webuser_admin),
    path("webuser/<str:id>/update/<str:mode>",views.webuser_update),
    path("webuser/<str:id>/delete/<str:mode>",views.webuser_delete),
    path("session",views.session),
    path("cookie",views.cookie),
   


]
