import random
import json
import requests
from bs4 import BeautifulSoup


proxies = {

}


headers = {'User-Agent': 'Mozilla/5.0'}


def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        if(url.find('https://item.jd.com/')!=-1):
            r.encoding ='utf-8'
    except:
        print("搜索失败")
        return ""
    return r.text


def getPrice(url):
    try:
        r = requests.get(url, headers=headers)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8';
        result=json.loads(r.text)
        price=result[0]['p']
    except:
        print("获取价格失败")
        return ""
    return price


def getUnivList(allUnivList,text,Limit):
    nums = 0

    bookUrls = []
    bookPriceURLs = []
    bookInfo = []  # 每件商品的信息 0价格  1  名字 2 评论数量   3图片     4 店名   5 平台  6物品详细界面 7筛选  8商品ID   9   前十标志 0

    soup = BeautifulSoup(text, "html.parser")
    bookIDs = soup.findAll('li', {'class': 'gl-item'}, limit=Limit)  # 获取书本ID
    length = len(bookIDs)
    if (length == 0): return ""    #如果搜索为空就直接返回
    commentNum = soup.findAll('div', class_='p-commit', limit=Limit)  # 获取评论数量
    img = soup.findAll('div', class_='p-img', limit=Limit)  # 获取图片

    for i in range(length):
        bookUrls.append('https://item.jd.com/' + str(bookIDs[i].get('data-sku')) + '.html')  # 把商品的url加入数列
        bookPriceURLs.append('https://p.3.cn/prices/mgets?skuIds=J_' + str(bookIDs[i].get('data-sku')))  # 把商品价格的url加入列表

    for i in range(length):  # bug ：获取的元素不存在时会出错 用#isinstance(div,bs4.element.Tag):  判断   没有就给个空字符串
        text = getHTMLText(bookUrls[i])
        if (text == ""): return ""  # 抓不到就返回空
        soup = BeautifulSoup(text, "html.parser")

        bookInfo.append(float(getPrice(bookPriceURLs[i])))  # 价格
        name = soup.findAll('div', class_='sku-name', limit=1)  # 名字(限制22个字)
        if(len(name)):
            if(len(str(name[0].text.strip()))<=21):
                bookInfo.append(str(name[0].text.strip()))
            else:
                bookInfo.append(str(name[0].text.strip())[0:21]+"...")
        else:
            bookInfo.append('')

        bookInfo.append(str(commentNum[i].text.strip()))  # 把评论数论数量加入列表

        if (str(img[i].img.get('src')) == 'None'):
            bookInfo.append('http:' + str(img[i].img.get('source-data-lazy-img')))  # 把图片加入列表
        else:
            bookInfo.append('http:' + str(img[i].img.get('src')))  # 把图片加入列表


        shopName = soup.findAll('div', class_='J-hove-wrap', limit=1)  # 店名

        if (len(shopName)):
            shopName = shopName[0].findAll('a', limit=1)  # 在任何一个标签上都可以使用 findAll（）
            if (len(shopName)):
                bookInfo.append(str(shopName[0].text.strip()))
            else:
                bookInfo.append('京东自营')
        else:
            bookInfo.append('')

        bookInfo.append("京东")
        bookInfo.append(bookUrls[i])
        bookInfo.append('1')
        bookInfo.append(str(bookIDs[i].get('data-sku')))
        allUnivList.append(bookInfo)
        bookInfo=[]

def jingdong(key,Limit,allUnivList):   #bug:当搜索不足10条时
    url = 'https://search.jd.com/Search?keyword=' + key + '&enc=utf-8&wq=' + key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)

    '''lenth=len(allUnivList)                  #如果没有关键字就过滤掉   弄一个由用户打开的过滤模式
    for i in range(lenth-1,-1,-1):
        if(allUnivList[i][1][:19].find(key)==-1):
            del allUnivList[i]'''






