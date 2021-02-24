import requests
import json
proxies = {

}
headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A5366a MicroMessenger/6.7.2 NetType/WIFI Language/zh_CN'
         ,"X-Requested-With":"XMLHttpRequest"}

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
        books=bookdetail['dt']['books']
    except:
        print("该关键字熊猫格子没有数据")
    lenth=len(books)
    if lenth==0:
        print("该关键字熊猫格子没有数据")
        return ""

    for book in books:
        if book['fs']==False:
            continue
        bookInfo.append(float(book['dp']))
        bookname = str(book['tl'])
        if (len(bookname) <= 22):
            bookInfo.append(bookname)
        else:
            bookInfo.append(bookname[0:22] + "...")
        bookInfo.append('满66包邮')
        bookInfo.append(str(book['img']))
        bookInfo.append('熊猫格子🐼')
        bookInfo.append('')
        bookInfo.append('')
        bookInfo.append('3')
        allUnivList.append(bookInfo)
        bookInfo=[]


def xiongmao(key,Limit):   #bug:当搜索不足10条时
    allUnivList=[]
    url = 'http://www.pandabox.top/luka/api/book/search/list?keyword='+key+'&pageNo=0&limit=20'
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text, Limit)
    return allUnivList
