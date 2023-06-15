from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import webUser

# Create your views here
def base(request):
    return render(request,"base.html",locals())

def css_index(request):
    return render (request,"cssindex.html",locals())
def index(request):
    return render(request,"index.html",locals())
def vip(request):
    if "username" in request.session:
        return HttpResponse("vip_page")
    else:
         return redirect("/api/vip_register")
def vip_register(request):

    return render(request,"vip_register.html",locals())
from django.db import connections
def webuser_showfield(request):
    cursor=connections["default"].cursor()
    sql ="select * from myapp_webuser "
    cursor.execute(sql,[])
    description=cursor.description
   # print(description)
    print("====================================")
    field_names=webUser._meta.get_fields()
    print(field_names)
    print(type(field_names))
    return render(request,"webuser_showfield.html",{"field_names":field_names})
def webuser_get_all(request):
    sql = "select * from myapp_webuser  "
    cursor =connections["default"].cursor()
    cursor.execute(sql,[])
    result=cursor.fetchall()
    return HttpResponse(result)
from datetime import date
def vip_user_add(request):
    if request.method == "POST":
        
        #用這個取值方法可以避免空值
        username_input = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm=request.POST.get("password_confirm")
        if password !=  password_confirm:
            return HttpResponse(" password error!!")
        else:
            try:
               
             phone = request.POST.get("phone")
             addr = request.POST.get("addr")
             hobit = request.POST.get("hobit")
             first_name = request.POST.get("first_name")
             last_name = request.POST.get("last_name")
             email = request.POST.get("email")
             superuser=0
             staff=0
             active=1
        
             cursor=connections["default"].cursor()


             sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
             sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
             sql %= (username_input,password,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

             cursor.execute(sql,[])
            except:
             return HttpResponse("account existed!!")
        return HttpResponse(" register success!!")

    else:
        return HttpResponse("Plz use Post method to input ur data")
def webuser_admin(request):
    #get all data from model of webuser first
    #pick all vlaues to del_page
    cursor = connections["default"].cursor()
    sql = "select * from myapp_webuser "
    #next sync will get object ,but not values
    cursor.execute(sql,[])
    #有需要查詢回傳才需要fetchall(),否則諸如insert into update delete都不需要這行指令
    result=cursor.fetchall()
    field_names =cursor.description
    #print("======field_names=====")
    #print(field_names)
    #print("====result========")
    #print(result)
    user_list=[]
    #print("=====dict_data")
    for  data in result:
        i=0
        dict_data={}
        for d in data:
            dict_data[field_names[i][0]]=d
            i=i+1
        print(dict_data)
        user_list.append(dict_data)
    print("==========user_list==========")
    print(user_list)
    
    
        
    return render(request,"webuser_admin.html",locals())
def webuser_delete(request,id=None,mode=None):
    userid=id
    cursor=connections["default"].cursor()
    if mode =="load":
        sql =" select * from myapp_webuser where id ='%s' "
        sql %= (userid)
        cursor.execute(sql,[])
        field_name=cursor.description
        result =cursor.fetchall()

        for  data in result:
            i=0
            field_data={}
            for d in data:
                field_data[field_name[i][0]]=d
                i=i+1
        return render(request,"vip_delete.html",locals())

    elif mode=="delete":
        sql ="delete from myapp_webuser  where id ='%s' "
        sql %= (userid)
        cursor.execute(sql,[])
        return redirect("/webuser_admin")
    else:
        return HttpResponse("wrong  path")
    

def webuser_delete_backup(request,id=None):
    userid=id
    cursor =connections["default"].cursor()
    sql = "select * from myapp_webuser where id = %s  " %(userid)
    
    cursor.execute(sql,[])
    result = cursor.fetchall()
    field_name=cursor.description
    field_data={}
    for data in result:
        i=0
        for d in data:
            field_data[field_name[i][0]]=d
            i=i+1
    print(field_data)
    return  render(request,"vip_delete.html",locals())
def deleted(request,id=None):
    userid=id
    cursor =connections["default"].cursor()
    sql ="DELETE from myapp_webuser  where id = %s "% (userid)
    cursor.execute(sql,[])
    return redirect("/webuser_admin")



def webuser_update(request,id=None,mode=None):
    #目前的設計方法是index按下update鈕時,將所有參數都帶到這個update頁面,然後再處理
    #update可以只更新想要的欄位
    #進判斷式前可以先連結settings.py設定的資料庫跟Django內的default資料庫
    userid=id
    cursor =connections["default"].cursor()
    #藉由帶參數mode的方式,可以讓進update頁面呈現兩種視覺,可以只設定一個相同的url path,一個是看到自己的資料,用的方法跟當資料送出時的頁面後,又使用同一個方法
    if mode == "update":
        #用.POST.gett("phone")方式取代POST["phone"]的方式,重點在避免出現空值所帶來的錯誤
        phone = request.POST.get("phone")
        password=request.POST.get("password")
        password_confirm=request.POST.get("password_confirm")
        addr = request.POST.get("addr")
        hobit = request.POST.get("hobit")
        #這裡使用password ==""  而不是password  is None是因為,空白也是值,所以用is None會得不到我們相要的結果
        #除非今天是一個response的結果,就可能有機會是空值,而不是空白,這時就可以用is None
        if password == "" or password_confirm == "" :
            return HttpResponse("Please enter your new password!")
        elif password != password_confirm:
            return HttpResponse("Password and password confirmation do not match!")
        else:
            #當不是空值就使用sql語法update set
        
            sql ="update myapp_webuser set  "
            sql += " password='%s', phone='%s', addr='%s', hobit='%s', date_joined=now() "
            sql += " where id ='%s'"
            sql %= (password,phone,addr,hobit,userid)
            print("&&&&&&&&&&&&&&&&&sql 語法&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(sql)
            #update myapp_webuser set   password='yrtgil215', phone='0988118281', addr='台中巿', hobit='Working', date_joined=now()  where id ='9'
            cursor.execute(sql,[])
            return redirect("/webuser_admin")
    elif mode == "load":
         #進來一樣想看到選定的使用者資料,所以這裡要先處理資料獲得
        userid = id
        
        sql = " select * from myapp_webuser  where id = %s   "% (userid) 
        #執行sql語法
        cursor.execute(sql,[])
        #撈取資料庫內資料,應該說同步資料庫資料,把Sql語法送過去,資料拿回來,這裡只看的到資料的值,也就是Value
        result= cursor.fetchall()
        #重新將資料放到字典裡,方便template取用
        #要將資料重新放值,必須先拿到欄位名,這樣才好分辨,用Cursor的屬性即可取得
        field_name=cursor.description

        dict_data={}
        i=0
    
        #找到的id不會重複,所以這裡只會拿到一筆資料,再怎麼迴圈也是一樣,但還是要迴圈取樣,因為取回的就是一個list
        for data in result:
            
            #這裡面就是字典裡的迴圈,遍歷每一個欄位屬性值,請注意,是值
            for d in data:
                #這裡就是用字典的屬性改值的方式去存值,但是屬性的KEY值名來自於剛剛用cursor獲得的,二維陣列,要在每個一維裡取第0個位置資料
                dict_data[field_name[i][0]]=d#這裡要放的是把值放回來指定的KEY值下
                i=i+1#這樣才能對每個不同的欄位放值
                #至此,就完成了字典的重新存值,但如果是多筆資料,可以考慮重新設定一個newlist來將所有的dict值存入
        return render(request,"vip_update.html",locals())
    #進來不是指定load及update路徑
    else:
         return HttpResponse("請選擇模式")
def session(request):
    return HttpResponse("session page")
def cookie(request):
    return HttpResponse("cookie page")
      
