from django.shortcuts import render
from rabbit import models
import json
import requests
import threading
import datetime
from bs4 import BeautifulSoup
from rabbit.views.jingdong import jingdong
from rabbit.views.tianmao import tianmao
from rabbit.views.douban import author
from rabbit.views.douban import doubanInfo
from rabbit.views.dangdang import dangdang
from rabbit.views.kongfuzi import kongfuzi
from rabbit.views.xiongmao import xiongmao
from rabbit.views.manyoujing import manyoujing
from rabbit.views.ebook import ebookAll
from rabbit.views.userLists import userLists
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


threadLock = threading.Lock()
threads = []

class myThread (threading.Thread):
    def __init__(self,function,key,number,allUnivList):
        threading.Thread.__init__(self)
        self.function = function
        self.key = key
        self.number = number
        self.allUnivList = allUnivList
    def run(self):
        # 获取锁，用于线程同步
        threadLock.acquire()
        self.function(self.key, self.number, self.allUnivList)
        # 释放锁，开启下一个线程
        threadLock.release()

proxies = {
    'http':'http://183.230.162.20:8060'
}

headers = {'User-Agent': 'Mozilla/5.0'}

number=15     #限制数量

def index(request):
    return render(request, 'rabbit/index.html')     # 1请求 2html界面（前两个必须） 3传递到前端的数据（dict类型）

def book(request,type,bookname):

       #1 新书 2二手书 3电子书
    if(bookname==""):
        return render(request, 'rabbit/index.html')      #重定向到主页
    key = bookname
    if( type=='1'):
        if request.GET.get('flag')=="1":
            allUnivList = newbook(bookname, number)    #需要添加  书名 作者的方式搜索
            return render(request, 'rabbit/fresh.html', {'booknames': allUnivList})
        return render(request, 'rabbit/RFBook.html',{'bookname':bookname})


    elif (type == '2'):
        if request.GET.get('flag')=="1":
            allUnivList = secondbook(bookname, number)
            return render(request, 'rabbit/twoFresh.html', {'booknames': allUnivList})
        return render(request, 'rabbit/RSBook.html',{'bookname':bookname})


    elif (type == '3'):
        if request.GET.get('flag') == "1":
            allUnivList = ebook(bookname)
            return render(request, 'rabbit/threeFresh.html', {'booknames': allUnivList})
        return render(request, 'rabbit/REBook.html', {'bookname': bookname})
    else:
        return render(request, 'rabbit/index.html')   #重定向到主页

def check(allUnivList,platformNum):
    bookInfo=[]
    for i in range(8):
        if (i == 3):
            bookInfo.append('../../static/rabbit/img/indexImg.png')
        elif (i == 7):
            bookInfo.append(str(platformNum))
        else:
            bookInfo.append('')
    allUnivList.append(bookInfo)

def newbook(key,number): # input:关键字，爬取数量    output:返回一个爬取内容列表    还需要添加数据为空的情况       使用多线程 #allUnivList.sort(key=(lambda x: x[0]))
    allUnivList = []
    allUnivList1 = []
    allUnivList2 = []
    allUnivList3 = []
    empty = []
    #Author=author(key)      #添加作者

    thread1 = myThread(jingdong,key,number,allUnivList1)
    thread2 = myThread(tianmao, key, number, allUnivList2)
    thread3 = myThread(dangdang, key, number, allUnivList3)

    thread1.start()
    thread2.start()
    thread3.start()

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    for t in threads:
        t.join()

    if allUnivList1:     #检测三个平台是否为空   并合并到allUnivList
        allUnivList = allUnivList1
    else:
        empty.append('1')

    if allUnivList2:     #检测三个平台是否为空   并合并到allUnivList
        allUnivList = allUnivList + allUnivList2
    else:
        empty.append('2')

    if allUnivList3:     #检测三个平台是否为空   并合并到allUnivList
        allUnivList = allUnivList+allUnivList3
    else:
        empty.append('3')

    if len(allUnivList)==0:
        empty.append('4')
        for i in empty:
            check(allUnivList, i)
        return allUnivList
    allUnivList.sort(key=(lambda x: x[0]))

    if(len(allUnivList)>=10):
        for i in range(0,10):
            allUnivList[i].append(', 4')
    else:
        for i in range(len(allUnivList)):
            allUnivList[i].append(', 4')

    for i in empty:
        check(allUnivList,i)

    return allUnivList

def douban(request):
    bookname=request.GET.get('bookname')
    allUnivList=doubanInfo(bookname)
    return render(request, 'rabbit/douban.html', {'allUnivList': allUnivList})

def secondbook(key,number):
    allUnivList = []
    empty=[]
    allUnivListKong=kongfuzi(key, number) # input:关键字，爬取数量    output:返回一个爬取内容列表   youlu(key, number)有路网
    if allUnivListKong:
        allUnivList = allUnivListKong
    else:
        empty.append('1')

    allUnivListMan=manyoujing(key, number)
    if allUnivListMan:
        allUnivList = allUnivList + allUnivListMan
    else:
        empty.append('2')

    allUnivListXiong=xiongmao(key, number)

    if allUnivListXiong:
        allUnivList = allUnivList + allUnivListXiong
    else:
        empty.append('3')

    if allUnivList=='':
        for i in empty:
            check(allUnivList, i)
        return ''
    allUnivList.sort(key=(lambda x: x[0]))
    for i in empty:
        check(allUnivList,i)

    return allUnivList

def ebook(key):
    allUnivList =ebookAll(key)
    return allUnivList

def addBook(request):
    if request.session.get('is_login', None):
        bookUrl=request.GET.get('bookUrl')
        platform = request.GET.get('platform')
        price=request.GET.get('price')
        bookname=request.GET.get('bookname')
        userName= request.session['user_name']


        new_book_item = models.bookList.objects.create()
        new_book_item.userName = userName
        new_book_item.bookID=bookUrl
        new_book_item.platform=platform
        new_book_item.price = price
        if(len(bookname)>9):
            new_book_item.bookname = bookname[0:13]+'...'
        else:
            new_book_item.bookname = bookname
        new_book_item.save()

        return HttpResponse("")
    return HttpResponse('未登录')


def about(request):
    return render(request, 'rabbit/about.html')

def my(request):
    if request.session.get('is_login', None):
        allUnivListjing=[]
        allUnivListdang = []
        allUnivListtian = []
        allUnivListkong = []
        allUnivLists=[]

        jingTotal=0
        dangTotal=0
        tianTotal=0
        kongTotal=0
        userName = request.session['user_name']

        time=datetime.datetime.now().strftime('%H')
        greet ='Hello'
        sentence = ""
        if (4<int(time)<12):
            greet="早上好"
            sentence = "希望相处的时光，能让你忘记疲惫"
        elif(12<=int(time)<18):
            greet = "下午好"
            sentence = "来一杯清凉的下午茶🍵"
        else:
            greet='晚上好'
            sentence = "晚上到了，整理下今天的成果吧😁"

        sentences=[]


        user_book_lists = models.bookList.objects.filter(userName=userName)
        if user_book_lists:

            bookInfo=[]
            bookInfos = []
            for user_book_list in user_book_lists:

                if(str(user_book_list.platform).strip()=='1'):     #数据顺序为   京东 当当 天猫 淘宝           书名  价格  url
                   bookInfo.append(user_book_list.bookname)
                   bookInfo.append(user_book_list.price)
                   bookInfo.append(user_book_list.bookID)
                   bookInfo.append(user_book_list.id)
                   allUnivListjing.append(bookInfo)
                   jingTotal=jingTotal+float(user_book_list.price)
                   bookInfo = []
                if (str(user_book_list.platform).strip() == '3'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListdang.append(bookInfo)
                    dangTotal = dangTotal + float(user_book_list.price)
                    bookInfo = []
                if (str(user_book_list.platform).strip() == '2'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListtian.append(bookInfo)
                    tianTotal = tianTotal + float(user_book_list.price)
                    bookInfo = []
                if (str(user_book_list.platform).strip() == '4'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListkong.append(bookInfo)
                    kongTotal = kongTotal + float(user_book_list.price)
                    bookInfo = []




            total=[round(jingTotal, 1),round(dangTotal, 1),round(tianTotal, 1),round(kongTotal, 1)]

            lenth1=len(allUnivListjing)
            lenth2=len(allUnivListdang)
            lenth3=len(allUnivListtian)
            lenth4=len(allUnivListkong)
            lenthMax=max(lenth1,lenth2,lenth3,lenth4)
            lenths=[lenth1,lenth2,lenth3,lenth4]

            if lenth1<lenthMax:
                for i in range(lenthMax-lenth1):
                    allUnivListjing.append('-')

            if lenth2<lenthMax:
                for i in range(lenthMax-lenth2):
                    allUnivListdang.append('-')

            if lenth3<lenthMax:
                for i in range(lenthMax-lenth3):
                    allUnivListtian.append('-')

            if lenth4<lenthMax:
                for i in range(lenthMax-lenth4):
                    allUnivListkong.append('-')

            for i in range(lenthMax):
                bookInfos=[allUnivListjing[i],allUnivListdang[i],allUnivListtian[i],allUnivListkong[i]]
                allUnivLists.append(bookInfos)

            return render(request, 'rabbit/my.html',{'allUnivLists':allUnivLists,'total':total,'lenthMax':lenthMax,'lenths':lenths,'userName':userName,
                                                     'greet':greet,'sentence':sentence})

        return render(request, 'rabbit/my.html',{'userName':userName,'greet':greet,'sentence':sentence})        #查询不到数据返回空
    return HttpResponseRedirect("/login")


def delete(request):
    ID = request.GET.get('ID')
    allUnivListjing = []
    allUnivListdang = []
    allUnivListtian = []
    allUnivListkong = []
    allUnivLists = []

    jingTotal = 0
    dangTotal = 0
    tianTotal = 0
    kongTotal = 0
    total=[]
    lenths=[]
    if ID:
        models.bookList.objects.filter(id=ID).delete()
        userName = request.session['user_name']
        user_book_lists = models.bookList.objects.filter(userName=userName)



        if user_book_lists:

            bookInfo = []
            bookInfos = []
            for user_book_list in user_book_lists:

                if (str(user_book_list.platform).strip() == '1'):  # 数据顺序为   京东 当当 天猫 淘宝           书名  价格  url
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListjing.append(bookInfo)
                    jingTotal = jingTotal + float(user_book_list.price)
                    bookInfo = []
                if (str(user_book_list.platform).strip() == '3'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListdang.append(bookInfo)
                    dangTotal = dangTotal + float(user_book_list.price)
                    bookInfo = []
                if (str(user_book_list.platform).strip() == '2'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListtian.append(bookInfo)
                    tianTotal = tianTotal + float(user_book_list.price)
                    bookInfo = []
                if (str(user_book_list.platform).strip() == '4'):
                    bookInfo.append(user_book_list.bookname)
                    bookInfo.append(user_book_list.price)
                    bookInfo.append(user_book_list.bookID)
                    bookInfo.append(user_book_list.id)
                    allUnivListkong.append(bookInfo)
                    kongTotal = kongTotal + float(user_book_list.price)
                    bookInfo = []

            total = [round(jingTotal, 1), round(dangTotal, 1), round(tianTotal, 1), round(kongTotal, 1)]

            lenth1 = len(allUnivListjing)
            lenth2 = len(allUnivListdang)
            lenth3 = len(allUnivListtian)
            lenth4 = len(allUnivListkong)
            lenthMax = max(lenth1, lenth2, lenth3, lenth4)
            lenths = [lenth1, lenth2, lenth3, lenth4]

            if lenth1 < lenthMax:
                for i in range(lenthMax - lenth1):
                    allUnivListjing.append('-')

            if lenth2 < lenthMax:
                for i in range(lenthMax - lenth2):
                    allUnivListdang.append('-')

            if lenth3 < lenthMax:
                for i in range(lenthMax - lenth3):
                    allUnivListtian.append('-')

            if lenth4 < lenthMax:
                for i in range(lenthMax - lenth4):
                    allUnivListkong.append('-')

            for i in range(lenthMax):
                bookInfos = [allUnivListjing[i], allUnivListdang[i], allUnivListtian[i], allUnivListkong[i]]
                allUnivLists.append(bookInfos)

            return render(request, 'rabbit/bookList.html',
                          {'allUnivLists': allUnivLists, 'total': total, 'lenths': lenths})
    return render(request, 'rabbit/bookList.html',
                  {'allUnivLists': allUnivLists, 'total': total, 'lenths': lenths})


def login(request):
    if request.session.get('is_login', None):    #如果session为空就再次重定向到登录界面
        return HttpResponseRedirect('/')

    if request.method=="POST":
        username=request.POST.get('username',None)
        password = request.POST.get('password', None)
        if username and password:
            username = username.strip()
            message=""
            try:
                user=models.User.objects.get(userName=username)
                if user.userPassword==password:
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name'] = user.userName
                    return HttpResponseRedirect('/')
                else:
                    message = '密码错误！'
            except:
                message='用户名不存在！'
            return render(request, 'rabbit/login.html', {"message": message})
    return render(request, 'rabbit/login.html')



def register(request):
    message=""
    '''if request.session.get('is_login', None):
        return HttpResponseRedirect('/')'''

    if request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if username and password and email:
            same_name_user = models.User.objects.filter(userName=username)
            if same_name_user:
                message='用户名已经存在'
                return render(request, 'rabbit/register.html', {"message": message})

            same_name_email = models.User.objects.filter(email=email)
            if same_name_email:
                message = '该邮箱地址已被注册'
                return render(request, 'rabbit/register.html', {"message": message})

            new_user = models.User.objects.create()
            new_user.userName = username
            new_user.userPassword = password
            new_user.email = email
            new_user.save()
            request.session['is_login'] = True
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.userName
            return HttpResponseRedirect('/')

    return render(request, 'rabbit/register.html')

def logout(request):
    if not request.session.get('is_login', None):
        #未登录，也就没有登出
        return HttpResponseRedirect("/")
    #request.session.flush()

    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return HttpResponseRedirect("/")

