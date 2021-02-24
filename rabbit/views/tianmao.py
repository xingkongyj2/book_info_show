
import requests
from bs4 import BeautifulSoup
import bs4

proxies = {
    'http':'http://221.2.175.238:8060'
}

headers = {'User-Agent': 'Mozilla/5.0'}


def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='gbk';
    except:
        print("淘宝搜索失败")
        return ""
    return r.text


def getUnivList(allUnivList,text,Limit):
    bookInfo = []  # 每件商品的信息 0价格  1  名字 2 评论数量   3图片     4 店名   5 平台  6物品详细界面 7筛选  8商品ID
    soup = BeautifulSoup(text, "html.parser")         #直接获取每一条数据的全部信息
    books = soup.findAll('div', class_='product', limit=Limit)  # 获取书本ID
    length = len(books)

    if (length == 0): return ""    #如果搜索为空就直接返回

    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            productPrice = book.findAll('p', class_='productPrice') #价格
            bookInfo.append(float(productPrice[0].text.replace("\n", "")[1:]))


            productTitle = book.findAll('p', class_='productTitle')  # 名字   限制22个字
            if (len(productTitle)):
                if (len(str(productTitle[0].text.strip())) <= 21):
                    bookInfo.append(str(productTitle[0].text.strip()))
                else:
                    bookInfo.append(str(productTitle[0].text.strip())[0:21] + "...")
            else:
                bookInfo.append('')


            productStatus = book.findAll('p', class_='productStatus')  # 评价
            bookInfo.append(str(productStatus[0].text))

            productImg = book.findAll('div', class_='productImg-wrap')  # 图片
            try:
                productImg = productImg[0].a.img['src']
            except:
                productImg = productImg[0].a.img['data-ks-lazyload']
            bookInfo.append('https:' + str(productImg))

            productShopName = book.findAll('a', class_='productShop-name')  # 店名
            bookInfo.append(str(productShopName[0].text))

            bookInfo.append('天猫')

            link = book.findAll('a', class_='productImg')  # 物品详细界面
            bookInfo.append('https:'+str(link[0]['href']))

            bookInfo.append('2')

            bookInfo.append(str(book['data-id']))

            allUnivList.append(bookInfo)
            bookInfo=[]                     #清空临时列表

def tianmao(key,Limit,allUnivList):   #bug:当搜索不足10条时
    url = 'https://list.tmall.com/search_product.htm?q='+ key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)

    '''lenth = len(allUnivList)
    for i in range(lenth - 1, -1, -1):
        if (allUnivList[i][1][:19].find(key) == -1):
            del allUnivList[i]'''


