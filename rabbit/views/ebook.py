import requests
from bs4 import BeautifulSoup
import bs4

proxies = {

}


headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Cookie":'sessionid=wplv193aex84mpp1sknyhj27bd3gdtmk; csrftoken=FJbuCEPObUYV3lsta85VKX6tD8Hz8LaDLAnowtR6Qj9TXh5n4NFjKvX0JHmX3MOX; Hm_lvt_375aa6d601368176e50751c1c6bf0e82=1544436946,1545919724,1546001336; Hm_lpvt_375aa6d601368176e50751c1c6bf0e82=1546005348',

}



def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers,proxies=proxies)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8';
    except:
        print(url+"搜索失败")
        return ""
    return r.text


def readfree(key,allUnivList):

    url="http://readfree.me/search/?q="+key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    soup = BeautifulSoup(text, "html.parser")

    books = soup.findAll('li', class_='book-item')  # 获取书本ID
    length = len(books)
    if (length == 0): return ""  # 如果搜索为空就直接返回

    bookInfo=[]
    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            temp = book.findAll('a', class_='pjax')  # 价格
            bookName=str(temp[1].text).strip()
            if (bookName.find(key)==-1):
                continue
            if len(bookName)<=32:
                bookInfo.append(bookName)
            else:
                bookInfo.append(bookName[0:32]+'...')
            bookInfo.append('http://readfree.me'+temp[1]['href'])
            bookInfo.append('Readfree')
            allUnivList.append(bookInfo)
            bookInfo=[]




def shuyu(key,allUnivList):
    url = "https://book.shuyuzhe.com/search/" + key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    soup = BeautifulSoup(text, "html.parser")

    books = soup.findAll('table', class_='table table-striped')[0]  # 获取书本ID
    books = books.findAll('tbody')[0]
    books = books.findAll('tr')
    length = len(books)
    if (length == 0): return ""  # 如果搜索为空就直接返回

    bookInfo = []
    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            book=book.findAll('a')[0]

            bookName = str(book['title']).strip()
            if (bookName.find(key) == -1):
                continue
            if len(bookName)<=32:
                bookInfo.append(bookName)
            else:
                bookInfo.append(bookName[0:32]+'...')
            bookInfo.append(book['href'])
            bookInfo.append('书语者')
            allUnivList.append(bookInfo)
            bookInfo = []






def skebooks(key,allUnivList):
    url="https://www.skebooks.com/q?type=1&keyword="+key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    soup = BeautifulSoup(text, "html.parser")

    books = soup.findAll('a', class_='book-tip') # 获取书本ID
    length = len(books)
    if (length == 0): return ""  # 如果搜索为空就直接返回

    bookInfo = []
    for book in books:
        if (isinstance(book, bs4.element.Tag)):

            bookName = str(book.text).strip()[3:]
            if (bookName.find(key) == -1):
                continue
            if len(bookName)<=32:
                bookInfo.append(bookName)
            else:
                bookInfo.append(bookName[0:32]+'...')
            bookInfo.append('https://www.skebooks.com' + book['href'])
            bookInfo.append('skebooks')
            allUnivList.append(bookInfo)
            bookInfo = []

def sobooks(key,allUnivList):
    url = "https://sobooks.cc/search/" + key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    soup = BeautifulSoup(text, "html.parser")

    books = soup.findAll('div', class_='shop-item')  # 获取书本ID
    length = len(books)
    if (length == 0): return ""  # 如果搜索为空就直接返回

    bookInfo = []
    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            book = book.findAll('div', class_='thumb-img focus')[0]
            book=book.contents[3]
            bookName = str(book['title']).strip()
            if (bookName.find(key) == -1):
                continue
            if len(bookName)<=32:
                bookInfo.append(bookName)
            else:
                bookInfo.append(bookName[0:32]+'...')
            bookInfo.append(book['href'])
            bookInfo.append("sobooks")
            allUnivList.append(bookInfo)
            bookInfo = []





def shuduoduo(key,allUnivList):
    url = "http://booksduo.com/?s=" + key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    soup = BeautifulSoup(text, "html.parser")

    books = soup.findAll('article', class_='excerpt excerpt-c5')  # 获取书本ID
    length = len(books)
    if (length == 0): return ""  # 如果搜索为空就直接返回

    bookInfo = []
    for book in books:
        if (isinstance(book, bs4.element.Tag)):
            book=book.findAll('h2')[0].contents[0]
            bookName = str(book.text).strip()
            if (bookName.find(key) == -1):
                continue
            if len(bookName)<=32:
                bookInfo.append(bookName)
            else:
                bookInfo.append(bookName[0:32]+'...')
            bookInfo.append(book['href'])
            bookInfo.append("书多多")
            allUnivList.append(bookInfo)
            bookInfo = []









def ebookAll(key):   #bug:当搜索不足10条时
    allUnivList = []
    #sobooks(key, allUnivList)
    #shuduoduo(key, allUnivList)
    skebooks(key,allUnivList)
    shuyu(key, allUnivList)
    return allUnivList

