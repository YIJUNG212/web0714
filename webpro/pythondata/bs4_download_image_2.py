import requests,bs4,os,urllib.parse
url ='http://aaa.24ht.com.tw/'
# url ='https://tw.yahoo.com/'
htmlFile =requests.get(url)

htmlFile.raise_for_status()
#以上是網頁前置,得回一個Response[200]的查詢集

headers={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"}

destDir ='out5_15'
if os.path.exists(destDir) == False:
    os.mkdir(destDir)
#以上為若資料夾不存在,就創建資料夾

#建立bs4.BeautifulSoup查詢物件

objSoup = bs4.BeautifulSoup(htmlFile.text,'lxml')

imgTag=objSoup.select('img')
# print(len(imgTag))

if len(imgTag) >0:
    for d in imgTag:
        imgUrl=d.get('src')
        # print(imgUrl)
        finUrl=urllib.parse.urljoin(url,imgUrl)
        # print(finUrl)
        picture=requests.get(finUrl,headers=headers, allow_redirects=True)
        picture.raise_for_status()
        # with open(os.path.join(destDir,os.path.basename(imgUrl)),'wb') as picFile:
        #     picFile.write(picture.content)
        #     picFile.close()
        pictFile=open(os.path.join(destDir,os.path.basename(imgUrl)),'wb')
        for diskStorage in picture.iter_content(10240):
            pictFile.write(diskStorage)
        pictFile.close()
        
       