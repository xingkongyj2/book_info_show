
import requests
import json
import random
proxies = {

}
headers = {'User-Agent': 'Mozilla/5.0'}

def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8';
    except:
        print("孔夫子搜索失败")
        return ""
    return r.text

def getFee(userId,itemId):
    fee=""
    url='http://shop.kongfz.com/book/shopsearch/getShippingFee?callback=jQuery11120008516125003493968_1545017785216&params={%22params%22:[{%22userId%22:%22'+userId+'%22,%22itemId%22:%22'+itemId+'%22}],%22area%22:%221006000000%22}'
    text=getHTMLText(url)
    if (text == ""): return "邮费获取失败"  # 抓不到就返回空
    text=text.replace('jQuery11120008516125003493968_1545017785216(','').replace(')','')
    feeAll = json.loads(text)
    try:
        fee='快递:'+feeAll['data'][0]['fee'][0]['totalFee']
    except:
        fee="无邮费信息"
    return fee

def getUnivList(allUnivList,text,Limit):
    bookdetail = json.loads(text)
    bookInfo = []  # 每件商品的信息 0价格  1  名字 2 评论数量(邮费)   3图片     4 店名   5 平台(商品的品数)  6物品详细界面 7筛选  8商品ID

    books=bookdetail['data']['itemList']
    lenth=len(books)
    if lenth==0:
        return "该关键字没有数据"
    if(lenth>Limit):
        lenth=Limit;
    for i in range(lenth):
        bookInfo.append(float(books[i]['price']))

        bookname=str(books[i]['itemname_snippet']).replace('<b>','').replace('</b>','')
        if (len(bookname) <= 22):
            bookInfo.append(bookname)
        else:
            bookInfo.append(bookname[0:22]+ "...")

        bookInfo.append(getFee(str(books[i]['userid']),str(books[i]['itemid'])))  #传入用户ID与商品ID去获得邮费
        if str((books[i]['imgurl']))=="":
            bookInfo.append("")
        else:
            bookInfo.append('http://www.kfzimg.com/'+str((books[i]['imgurl'])))
        bookInfo.append(str(books[i]['shopname'])[0:15])
        bookInfo.append(str(books[i]['qualityname']))
        bookInfo.append('http://book.kongfz.com/'+str(books[i]['shopid'])+'/'+str(books[i]['itemid'])+'/')
        bookInfo.append('1')
        allUnivList.append(bookInfo)
        bookInfo=[]


def kongfuzi(key,Limit):   #bug:当搜索不足10条时
    allUnivList=[]
    url = 'http://search.kongfz.com/product_result/?key='+key+'&type=1&ajaxdata=1'
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)

    return allUnivList