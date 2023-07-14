import requests
url ='https://www.gzaxxc.com/file_not_existed'

try:
    htmlfile =requests.get(url)
    print("下戴成功") 
except Exception as err:
    print("網頁下載失敗:%s"% err)
print("程式結束")