import bs4,requests,os,urllib.parse
# url ='http://homepi.myftp.org:8000/index'
url ='https://tw.yahoo.com/'


html =requests.get(url)
print("網頁下載中....")
html.raise_for_status()
print("網頁下載完成")
objSoup =bs4.BeautifulSoup(html.text,'lxml')
img_obj=objSoup.find_all('img')
if len(img_obj)>0:
    
    for data in img_obj:
        src_obj=data.get("src")#用get()取值才不會在值不存在時出例外,這時是取出圖片的相對src位置
        finUrl =urllib.parse.urljoin(url,src_obj)#用urljoin的方法,組合出真正的圖片位置
        picture=requests.get(finUrl)#用找到的圖片位置去獲得每張圖的物件
        picture.raise_for_status()
        print("圖片物件本體是什麼類型",type(picture))
        print("文字text",picture.text)
        print("二維編碼content",picture.content)

        
        
     