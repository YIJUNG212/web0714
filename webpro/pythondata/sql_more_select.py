import mysql.connector
Mydb =mysql.connector.connect(
    host="localhost",
    user="seric",
    password="yrtgil212",
    
)

cursor =Mydb.cursor()#連結資料庫,這時沒有選資料庫
# sql ="select * from pythonsql.sql1  where name= %s "#從指定資料庫及資料表撈所有資料
# cursor.execute(sql,("Marry",))#執行語法
# result=cursor.fetchall()#賦值s

# sql="select * from pythonsql.sql1 where name like %s "
# cursor.execute(sql,("%M%",))
# result=cursor.fetchall()

#使用order by

sql ="select * from pythonsql.sql1   where name like %s order by address   "
cursor.execute(sql,("%M%",))
result=cursor.fetchall()
for d in result:
    print(d)
