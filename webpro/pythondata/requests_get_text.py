import requests
url ='https://google.com.tw'
htmlpage =requests.get(url)
if htmlpage.status_code == 200:
    print("網頁資料有取得")
else:
    print("網頁資料沒有取得")
print(htmlpage.text)