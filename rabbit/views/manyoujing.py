

import requests
import json
proxies = {

}
headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN'
         ,'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NDUzNzI1MzAsInVpZCI6IllBNzZOb04xIn0.YVlHbgzfO_9W0y-qdUYybZpGC2shJJT9wYPBLFI9Ko8'
}

def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8';
    except:
        print("漫游鲸搜索失败")
        return ""
    return r.text


def getUnivList(allUnivList,text,Limit):
    bookdetail = json.loads(text)
    bookInfo = []  # 每件商品的信息 0价格  1  名字 2 评论数量(邮费)   3图片     4 店名   5 平台(商品的品数)  6物品详细界面 7筛选  8商品ID
    books=[]
    try:
        books=bookdetail['data']
    except:
        print('该关键字漫游鲸没有数据')
    lenth=len(books)
    if lenth==0:
        print('该关键字漫游鲸没有数据')
        return ""

    for book in books:
        if book['sold_out']==True:
            break
        bookInfo.append(float(book['price']))
        bookname = str(book['title'])
        if (len(bookname) <= 22):
            bookInfo.append(bookname)
        else:
            bookInfo.append(bookname[0:22] + "...")
        bookInfo.append('满69包邮')
        bookInfo.append('https://img3.doubanio.com/lpic/'+str(book['image'])[48:])
        bookInfo.append('漫游鲸🐳')
        bookInfo.append('漫游鲸🐳')
        bookInfo.append('')
        bookInfo.append('2')
        allUnivList.append(bookInfo)
        bookInfo=[]

def manyoujing(key,Limit):   #bug:当搜索不足10条时
    allUnivList=[]
    url = 'https://app.manyoujing.net/v1/book/search?keyword='+key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)
    return allUnivList
