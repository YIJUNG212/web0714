import requests,bs4
# url ='http://www.deepmind.com.tw'
url='http://homepi.myftp.org:8000/index'
htmlFile= requests.get(url)
objSoup=bs4.BeautifulSoup(htmlFile.text,'lxml')
print("列印BeautifulSoup物件資料型態",type(objSoup))
# print(objSoup.title)
# print(objSoup.title.text)
# # print(objSoup.p1)
# print(objSoup.a)
# objtag=objSoup.find('a')
# print(objtag)
#上面的用標籤名跟用find()標籤名,結果一樣.但如果用findall()就要用迴圈取值了

tagall=objSoup.find_all('a')
for data in tagall:
    # print(data.text)
    print(data.getText())
    
    
    
# print(objSoup.input)
# print(objSoup.div)
# print(objSoup.section)
# print(objSoup.nav)