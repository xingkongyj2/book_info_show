
import requests
from bs4 import BeautifulSoup
import bs4


proxies = {

}

headers = {'User-Agent': 'Mozilla/5.0'}


def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='gbk';
    except:
        print("当当搜索失败")
        return ""
    return r.text

def getUnivList(allUnivList,text,Limit):

    bookInfo = []  # 每件商品的信息 0价格  1  名字 2 评论数量   3图片     4 店名   5 平台  6物品详细界面 7筛选  8商品ID

    soup = BeautifulSoup(text, "html.parser")         #直接获取每一条数据的全部信息
    books = soup.findAll('ul', class_='bigimg',limit=1)  # 获取每一本的信息
    try:
        books = books[0].findAll('li',limit=Limit)
    except:
        print('当当没有该关键字数据')
        books=[]
    length = len(books)
    if (length == 0): return ""    #如果搜索为空就直接返回

    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            productPrice = book.findAll('span', class_='search_now_price') #价格
            bookInfo.append(float(productPrice[0].text[1:]))

            productTitle = book.findAll('p', class_='name')  # 名字
            if (len(productTitle)):
                if (len(str(productTitle[0].text.strip())) <= 20):
                    bookInfo.append(str(productTitle[0].text.strip()))
                else:
                    bookInfo.append(str(productTitle[0].text.strip())[0:20] + "...")
            else:
                bookInfo.append('')

            productStatus = book.findAll('p', class_='search_star_line')  # 评价
            bookInfo.append(str(productStatus[0].text))

            productImg = book.findAll('a', class_='pic')  # 图片
            link=productImg[0]['href']                      #获取物品详细界面
            try:
                productImg = productImg[0].img['data-original']
            except:
                productImg = productImg[0].img['src']
            bookInfo.append(str(productImg))

            productShopName = book.findAll('p', class_='search_shangjia')  # 店名   分自营和商家   限制22个字
            if (len(productShopName)):
                productShopName = productShopName[0].find('a')['title']
                bookInfo.append(productShopName)
            else:
                bookInfo.append('当当自营')

            bookInfo.append('当当')

            bookInfo.append(link)

            bookInfo.append('3')

            bookInfo.append(book['id'][1:])

            allUnivList.append(bookInfo)
            bookInfo = []


def dangdang(key,Limit,allUnivList):   #bug:当搜索不足10条时
    url = 'http://search.dangdang.com/?key='+key+'&act=input'
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)

    '''lenth = len(allUnivList)
    for i in range(lenth - 1, -1, -1):
        if (allUnivList[i][1][:19].find(key) == -1):
            del allUnivList[i]'''
