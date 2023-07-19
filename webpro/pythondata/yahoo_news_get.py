import requests,bs4,re
url ="https://tw.yahoo.com/"
htmlFile =requests.get(url)
objSoup =bs4.BeautifulSoup(htmlFile.text,'lxml')
# headline_news = objSoup.select('a.active_V\\(v\\)')
headline_news = objSoup.find_all('a', class_=r'active_V(v)')
print(headline_news[0])#只列第一組目標
# print(headline_news[0].text)


# for h in headline_news:
#     print(h)
#     print("焦點新聞:  " +h.text)
#     print("新聞網址:  "+h.get('href'))