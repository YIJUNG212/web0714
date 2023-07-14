import requests
import re
url ='https://www.mcut.edu.tw'
htmlpage =requests.get(url)
pattern =input("請輸入查詢字樣:   ")
if htmlpage.status_code == 200:
    print("有拿到網頁資料")
        #用re.findall()將找到資料放在list裡返回
    name =re.findall(pattern,htmlpage.text)
    if name != None:
        print("%s 出現次數"%pattern,len(name))
    else:
        print("找不到  %s "%pattern)
else:
   print("沒有拿到網頁資料")
