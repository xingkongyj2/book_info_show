
from django.urls import path, re_path

from . import views

app_name = 'rabbit'
urlpatterns = [



    path('newbook/', views.newbook,name='newbook'),



    #path(r'index/', views.index),     # 匹配空字符串^$    注意斜杆/问题
    #re_path(r'^article/(?P<article_id>\d+)/$', views.article_page,name='article_page'),
    #re_path(r'^edit/(?P<article_id>\d+)/$', views.edit_page,name='edit_page'),
    #path(r'edit/action', views.edit_action,name='edit_action'),
]


