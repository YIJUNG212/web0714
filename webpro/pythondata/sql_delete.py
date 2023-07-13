import mysql.connector

Mydb=mysql.connector.connect(
    host="localhost",
    user="seric",
    password="yrtgil212",
)

cursor=Mydb.cursor()

sql_del ="delete from pythonsql.sql1 where id = %s"
cursor.execute(sql_del,("2",))
Mydb.commit()

sql_showall ="select * from pythonsql.sql1  "
cursor.execute(sql_showall)
result =cursor.fetchall()
for d in result:
    print(d)