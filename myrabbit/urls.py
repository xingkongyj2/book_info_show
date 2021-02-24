"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include,re_path
from rabbit.views import index

import rabbit.views as bv     #引用写的函数



urlpatterns = [
    path('manage/', admin.site.urls),     #使用Function views方法来配置url   三个参数：url本身（一个地址）  响应函数   url名称

    re_path('^$', index.index,name='index'),

    re_path(r'^(?P<type>.*)&(?P<bookname>.*)$', index.book,name='bookname'),   #配置一个总路径  urls文件里的是子路径

    path('addBook',index.addBook),

    path('doubanInfo', index.douban),

    path('about',index.about),

    path('my',index.my),

    path('login',index.login),

    path('register',index.register),

    path('logout', index.logout),

    path('delete', index.delete),




]
