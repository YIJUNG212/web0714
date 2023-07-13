import mysql.connector
Mydb =mysql.connector.connect(
    host="localhost",
    user="seric",
    password="yrtgil212",
    
)
sql=Mydb.cursor()
#sql.execute("create  schema if not exists  pythonsql") 創建資料表
sql.execute("show databases ")
#print(sql)  如果連結後直接列印本身,就會顯示object本體,也就是show databases
for x in sql:
    print(x)