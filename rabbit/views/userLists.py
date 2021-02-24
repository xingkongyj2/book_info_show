

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
        r.encoding ='utf-8'
    except:
        print("搜索失败")
        return ""
    return r.text


def getPrice(url):
    try:
        r = requests.get(url, headers=headers)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8'
        result=json.loads(r.text)
        price=result[0]['p']
    except:
        print("获取价格失败")
        return ""
    return price


def getUnivListjing(allUnivList):

    bookUrls = []
    bookPriceURLs = []


    for i in range(length):
        bookUrls.append('https://item.jd.com/' + str(bookIDs[i].get('data-sku')) + '.html')  # 把商品的url加入数列
        bookPriceURLs.append('https://p.3.cn/prices/mgets?skuIds=J_' + str(bookIDs[i].get('data-sku')))  # 把商品价格的url加入列表

def getUnivListdang(allUnivList):

    bookUrls = []
    bookPriceURLs = []


    for i in range(length):
        bookUrls.append('https://item.jd.com/' + str(bookIDs[i].get('data-sku')) + '.html')  # 把商品的url加入数列
        bookPriceURLs.append('https://p.3.cn/prices/mgets?skuIds=J_' + str(bookIDs[i].get('data-sku')))  # 把商品价格的url加入列表


def getUnivListkong(allUnivList):

    bookUrls = []
    bookPriceURLs = []


    for i in range(length):
        bookUrls.append('https://item.jd.com/' + str(bookIDs[i].get('data-sku')) + '.html')  # 把商品的url加入数列
        bookPriceURLs.append('https://p.3.cn/prices/mgets?skuIds=J_' + str(bookIDs[i].get('data-sku')))  # 把商品价格的url加入列表

def getUnivListtian(allUnivList):

    bookUrls = []
    bookPriceURLs = []


    for i in range(length):
        bookUrls.append('https://item.jd.com/' + str(bookIDs[i].get('data-sku')) + '.html')  # 把商品的url加入数列
        bookPriceURLs.append('https://p.3.cn/prices/mgets?skuIds=J_' + str(bookIDs[i].get('data-sku')))  # 把商品价格的url加入列表


def userLists(bookUrl):
    allUnivList=[]
    for url in bookUrl:
        text=getHTMLText(url)
        if (text == ""): return ""  # 抓不到就返回空
        (text)

    return allUnivList