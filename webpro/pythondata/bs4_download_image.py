import bs4,requests,os,urllib.parse
# url ='http://homepi.myftp.org:8000/index'
url ='https://tw.yahoo.com/'


html =requests.get(url)
print("網頁下載中....")
html.raise_for_status()
print("網頁下載完成")
destDir ="out5_14"
if os.path.exists(destDir) == False:
    os.mkdir(destDir)
objSoup =bs4.BeautifulSoup(html.text,'lxml')
imgTag =objSoup.select('img')
# print("對應到的bs4格式",objSoup)
print(objSoup)
print("搜尋到的圖片數量",len(imgTag))
if len(imgTag) >0:
    for i in range(len(imgTag)):
        imgUrl =imgTag[i].get('src')#每張圖都有對應的src url ,所以要一一撈出來
        print("%s 圖片下載中...."%imgUrl)
        # finUrl=url+imgUrl#重新組合每張圖片的url,這裡的url 是指對應到根目錄的位置
        finUrl = urllib.parse.urljoin(url, imgUrl)
        print("%s 圖片下載中...."%finUrl)
        picture=requests.get(finUrl)#重新得到每一個物件,這時得到的就是圖像本身
        picture.raise_for_status()
        print("%s 圖片下載成功"%finUrl)
        #先開啟檔案，再儲存圖片
        #因為圖片是二進制的,所以要用wb來存
        # pictFile =open(os.path.join(destDir,os.path.basename(imgUrl)),'wb')
        # for diskStorage in picture.iter_content(10240):#這裡在iter_content()裡應該表示每一個pixels
        #     pictFile.write(diskStorage)#將每個像素都寫入檔案裡
        # pictFile.close()#存完以後關掉檔案
        
        #另外的寫法
        imgPath =os.path.join(destDir,os.path.basename(imgUrl))
        with open(imgPath,'wb') as f:
            f.write(picture.content)#content代表的是不轉碼的ascii碼,所以可以寫入圖像或音訊
        f.close()
print("圖片下載完成")
        
        
     