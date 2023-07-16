import requests

url= 'http://www.deepmind.com.tw'
try:
    htmlfile =requests.get(url)
    print('下載成功')
    print(htmlfile.status_code)
    print(htmlfile.text)
except Exception as error:
    print("下載失敗: %s"% error )
    
fn ='out3_14.txt'
with open(fn,'wb') as file_Obj:#將開啟的檔案取別名是一個物件名
    for diskStorage in htmlfile.iter_content(40960):
        size=file_Obj.write(diskStorage)
        print(size)
    print("以%s儲存網頁TML檔案成功"%fn)