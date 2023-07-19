import requests,bs4
url ='ch5_2_1.html'
htmlFile =open(url,encoding='utf-8')
objSoup=bs4.BeautifulSoup(htmlFile,'lxml')
titleobj=objSoup.find_all('h2')
itemobj=objSoup.find('ol',type='I')
items =itemobj.find_all('li')
for item in items:
    print(item.text)
