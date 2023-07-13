import mysql.connector
Mydb =mysql.connector.connect(
    host="localhost",
    user="seric",
    password="yrtgil212",
)

cursor=Mydb.cursor()

sql_showall="select * from pythonsql.sql1 where name like %s order by name desc limit 5 offset 2   "
cursor.execute(sql_showall,("%M%",))
result=cursor.fetchall()
for d in result:
    print(d)