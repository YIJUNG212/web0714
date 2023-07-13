import json

login =input("請輸入帳號:")
file='login.json'
with open(file,'w') as loginObj:
    json.dump(login,loginObj)
print("歡迎光臨"+login)
print("歡迎光臨",login)
print("歡迎光臨%s"%login)