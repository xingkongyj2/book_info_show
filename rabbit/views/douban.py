
import json
import requests

proxies = {
    #'http':'http://117.135.153.10:80'
}

headers = {'User-Agent': 'Mozilla/5.0'}

def getHTMLText(url):   #通用 获取网页信息
    try:
        r = requests.get(url, headers=headers)   #设置代理 设置时间
        r.raise_for_status()
        r.encoding ='utf-8';
    except:
        print("豆瓣API调用失败")
        return ""
    return r.text

#0名字 1评分  2时间 3标签1  4标签2  5图片  6内容简介  7作者  8出版社 9url
def getUnivList(allUnivList,text):
     bookdetail=json.loads(text)
     try:
         if (len(bookdetail['books'][0]['title'])>=25):
            allUnivList.append(bookdetail['books'][0]['title'][0:25]+"...")
         else:
             allUnivList.append(bookdetail['books'][0]['title'])
         allUnivList.append(bookdetail['books'][0]['rating']['average'])
         allUnivList.append(bookdetail['books'][0]['pubdate'][0:4])
         allUnivList.append(bookdetail['books'][0]['tags'][2]['name'])
         allUnivList.append(bookdetail['books'][0]['tags'][3]['name'])
         allUnivList.append('https://images.weserv.nl/?url='+bookdetail['books'][0]['image'][8:])
         if (len(bookdetail['books'][0]['summary']) >= 170):
             allUnivList.append(bookdetail['books'][0]['summary'][0:170]+"....")
         else:
             allUnivList.append(bookdetail['books'][0]['summary'])
         allUnivList.append(bookdetail['books'][0]['author'][0])
         allUnivList.append(bookdetail['books'][0]['publisher'])
         allUnivList.append(bookdetail['books'][0]['alt'])
     except:
         add=10-len(allUnivList)
         for i in range(0,add):
             allUnivList.append('')

def author(key):
    author=""
    url = 'https://api.douban.com/v2/book/search?q=' + key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    bookdetail = json.loads(text)
    try:
        author=bookdetail['books'][0]['author'][0]
        if (author.find('[')!=-1 and author.find(']')!=-1):
            author=author[3:]
        if (author.find('【')!=-1 and author.find('】')!=-1):
            author=author[3:]
    except:
        print("获取书籍作者失败")

    return author

def doubanInfo(key):   #bug:当搜索不足10条时
    allUnivList=[]
    url = 'https://api.douban.com/v2/book/search?q='+ key
    text = getHTMLText(url)
    if (text == ""): return ""  # 抓不到就返回空
    getUnivList(allUnivList, text)
    return allUnivList

