import mysql.connector
Mydb =mysql.connector.connect(
    host="localhost",
    user="seric",
    password="yrtgil212",
    database="pythonsql",
)

sql=Mydb.cursor()#這時候才可以操作資料庫
#sql.execute("create table if not exists sql1 (id int auto_increment primary key , \
#            name varchar(255),address varchar(255))")   目前這種寫法不利重複利用sql語句

#插入資料 下面寫法容易被攻擊
#sql_insert="insert into sql1(name,address) values('john','Taoyuan') "

# sql_insert2 ="insert into sql1(name,address) values(%s,%s) "
# value=("Marry","Kauhsiung")
# sql.execute(sql_insert2,value)
# Mydb.commit()

val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]
# sql_insert2 ="insert into sql1(name,address) values(%s,%s) "
# sql.executemany(sql_insert2,val)
# Mydb.commit()
sql_show_table ="select * from sql1 "
sql.execute(sql_show_table)
one =sql.fetchone()
print(one)
two =sql.fetchone()
print(two)
# for x in one:
#     print(x  )



