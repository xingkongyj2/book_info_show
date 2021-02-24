
import random
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
proxies = {
    'http':'http://183.230.162.20:8060'
}                                #注意http 和 https
#'http':'http://183.230.162.20:8060'
#'http':'http://124.89.174.199:8060'

def getProxies():
    url='https://www.kuaidaili.com/free/intr/1/'
    try:
        r = requests.get(url, headers=headers)   #设置代理 设置时间
        r.raise_for_status()
        if(url.find('https://item.jd.com/')!=-1):
            r.encoding ='gbk';
        else:r.encoding ='utf-8';
    except:
        print("爬取失败")
    soup = BeautifulSoup(r.text, "html.parser")
    ipLists = soup.findAll('tbody',limit=1)
    ipLists=ipLists[0].findAll('tr')
    ipListsRandom=random.randint(0,14)
    proxies['http']='http://'+ipLists[ipListsRandom].contents[1].string+':'+ipLists[ipListsRandom].contents[3].string
    return proxies

def cheakProxies():
    # 用来检测代理是否成功
    try:
        r = requests.get('http://icanhazip.com', headers=headers, proxies=proxies)
        r.raise_for_status()
    except:
        print("代理失败")
    print(r.text)
    print('代理成功')
