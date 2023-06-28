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

#要導入media需要使用的import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("base",views.base),
    path("css_index",views.css_index),
    path("index",views.index),
    path("api/vip",views.vip),
    path("vip_register",views.vip_register),
    path("api/vip_user_add",views.vip_user_add),
    path("webuser_showfield",views.webuser_showfield),
    path("webuser_get_all",views.webuser_get_all),
    path("webuser_admin",views.webuser_admin),
    path("webuser/<str:id>/update/<str:mode>",views.webuser_update),
    path("webuser/<str:id>/delete/<str:mode>",views.webuser_delete),
    path("set_cookie/<str:key>/<str:value>",views.set_cookie),
    path("get_cookie/<str:key>",views.get_cookie),
    path("get_cookie_all",views.get_cookie_all),
    path("set_cookie_time/<str:key>/<str:value>",views.set_cookie_time),
    path("del_cookie/<str:key>",views.del_cookie),
    path("set_session/<str:key>/<str:value>",views.set_session),
    path("get_session/<str:key>",views.get_session),
    path("get_session_all",views.get_session_all),
    path("del_session/<str:key>",views.del_session),
    path("login",views.login),
    path("logout",views.logout),
    path("login2",views.login2),
    path("login3",views.login3),
    path("accounts/index",views.index_django),
    path('register_django', views.sign_up, name='Register'),
    path("accounts/login",views.sign_in),
    path("logout_django",views.log_out_django),
    path("test",views.test),
    path("upload_image", views.upload_product_sql),
    path("upload_show",views.upload_show),
    path("shopitem",views.get_shopitem),
    path("product_buy",views.product_buy),
    path("product_select/<str:id>",views.buy_select),
    path("shopcar",views.shopcar_add),
    path("shopcar_show",views.shopcar_show),
    path("shopitem_action",views.shopitem_action),
   
    
  


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

