import requests ,bs4
url = 'http://www.taiwanlottery.com.tw/'
htmlobj =requests.get(url)
print("網頁下載中...")
htmlobj.raise_for_status()
print("網頁下載完成")
htmltext=htmlobj.text
soupobj=bs4.BeautifulSoup(htmltext,'lxml')
dataTag=soupobj.select(".contents_box02")# 查找的是class名,別忘了加.符號
print(len(dataTag))

for i in range(len(dataTag)):
   print(dataTag[i])
balls=dataTag[0].find_all("div",{"class":"ball_tx ball_green"})
print("開出順序: ",end="")
for i in range(6):#查找0至5
    print(balls[i].text,end=" ")#列出每個標籤包裏的值