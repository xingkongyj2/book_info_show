from django.contrib import admin

from .models import User         #引用数据
from .models import bookList

class BlogAdmin(admin.ModelAdmin):  # 配置类 选择要展示的字段
    list_display=('id', 'userName', 'userPassword','email','loginNum','userCreat')   #list_display支持list tuple
    #list_filter = ('',)                          # 注意这里是一个元组类型

admin.site.register(User,BlogAdmin)        #把数据注册


class BlogAdmin2(admin.ModelAdmin):  # 配置类 选择要展示的字段
    list_display=('userName', 'bookname','price','platform', 'bookID','addTime')   #list_display支持list tuple

admin.site.register(bookList,BlogAdmin2)