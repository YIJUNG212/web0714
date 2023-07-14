import requests
# current_html = requests.get("https://google.com.tw/")
# print(current_html)  若有回應,會列回應碼200


#檢視status.code

url ='http://www.google.com.tw'

htmlfile = requests.get(url)
# if htmlfile.status_code == requests.codes.ok:
if htmlfile.status_code == 200:
    #print("取得網頁內容成功")
    print(htmlfile.text)
else:
    print("取得網頁內容失敗")