import json
fn ='login1_13.json'
try:
    with open(fn) as fnObj:
        login=json.load(fnObj)
except:
    login =input("請輸入帳號: ")
    with open(fn,'w') as fnObj:
        json.dump(login,fnObj)
        print("系統已經記錄你的帳號")
else:
    print("%s歡迎回來"%login)