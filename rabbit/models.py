from django.db import models


#字段就是类里面属性（变量）
#https://www.cnblogs.com/yelin/p/6253775.html
#https://docs.djangoproject.com/en/2.1/ref/models/fields/
#创建之后要数据迁移  1 python3 manage.py makemigrations app名（可选） 2 python3 manage.py migrate
#写入数据
#views.py 中import models

class User(models.Model):   #用户名 密码 邮箱 用户创建时间
    userName=models.CharField(max_length=100,unique=True)
    userPassword=models.CharField(max_length=32)
    email=models.EmailField(unique=True)
    loginNum=models.CharField(max_length=32,default="0")
    userCreat=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userName


class bookList(models.Model):   #用户名 密码 邮箱 用户创建时间
    userName=models.CharField(max_length=100)
    bookID=models.CharField(max_length=300)
    price=models.CharField(max_length=32)
    platform=models.EmailField(max_length=32)
    bookname = models.EmailField(max_length=100)
    addTime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userName


