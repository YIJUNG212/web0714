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

#新增一個哈希法的密碼生成
from django.contrib.auth.hashers import make_password
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
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        addr = request.POST.get("addr")
        hobit = request.POST.get("hobit")
        #這裡使用password ==""  而不是password  is None是因為,空白也是值,所以用is None會得不到我們相要的結果
        #除非今天是一個response的結果,就可能有機會是空值,而不是空白,這時就可以用is None
        #當傳送過來的密碼是空值時,就套用資料庫內的密碼
        if password =="":
            password = request.user.password
            password_confirm=password
            #當有新的輸入密碼,就將密碼換成新輸入的
        else:
            password=request.POST.get("password")
            password_confirm=request.POST.get("password_confirm")
        if password == "" or password_confirm == "" :
            return HttpResponse("Please enter your new password!")
        elif password != password_confirm:
            return HttpResponse("Password and password confirmation do not match!")
        else:
            #當不是空值就使用sql語法update set
            # 將密碼轉換為哈希值
            hashed_password = make_password(password)
        
            sql ="update myapp_webuser set  "
            sql += " password='%s', phone='%s', addr='%s', hobit='%s',first_name='%s',last_name='%s', date_joined=now() "
            sql += " where id ='%s'"
            sql %= (hashed_password,phone,addr,hobit,first_name,last_name,userid)
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

def set_cookie(request,key=None,value=None):
    print(key+" :"+value)
    #下面這行重點不在於reponse設定的是什麼訊息,重點是這個語法就可以將http回應回來的物件接住
    response = HttpResponse("set_cookie ok!!")
    #接到物件後,才能使用方法set_cookie()來設定kv值
    response.set_cookie(key,value)
    return response
def get_cookie(request,key=None):
    if key in request.COOKIES:
        return HttpResponse("%s : %s" %(key,request.COOKIES[key]))
    else:
        return HttpResponse(key +"isn't exist!!!")
def get_cookie_all(request):
    allcookie = request.COOKIES.items()
    #以上就可以獲得所有cookie
    #以下是客製化cookie的呈現方式
    #設定變數記得都先初始化空值情況
    cookie_show_style =""
    #用這種方式去找kv值,而且順便設定變數名,這個有前後關係
    for key,value in request.COOKIES.items():
        cookie_show_style=cookie_show_style+key+" : "+value+"<br>"


    return HttpResponse(cookie_show_style)
      
def set_cookie_time(request,key=None,value=None):
    response =HttpResponse("set cookie time ok")
    #這裡的3600單位是秒,代表著3600秒後會過期失效
    response.set_cookie(key,value,max_age=3600)
    return response
def del_cookie(request,key=None):
    #下面的寫法會出錯,因為這不是一個完整的http回應回來的物件,不能使用delete_cookie方法
    # reponse = request.COOKIES[key]
    # reponse.delete_cookie(key)
    #下面的寫法不能在key值不存在時有判斷,所以也不是最好的寫法
    # response =HttpResponse(key+" is deleted!!")
    # response.delete_cookie(key)
    if key in request.COOKIES:
        response =HttpResponse(key +" is deleted!!")
        return response
    else:
        return HttpResponse(key+" is not exist!!")
    
def set_session(request,key=None,value=None):
    #一樣要先接http的回應物件，這裡變成可設定可不設定，因為主要還是用request來啟動
    response = HttpResponse("session is saved!!")
    #跟cookie的存值方式略有不同,這裡是用request來啟動,不是用接回來的物件啟動
    request.session[key]=value
    return response
def get_session(request,key=None):
    if key in request.session:
        #取值的方式跟cookiey就沒什麼兩樣了
        return HttpResponse("%s  :  %s" %(key,request.session[key]))
    else:
        return HttpResponse( " no session :"+key)
def get_session_all(request):
    #一樣有items()的方法,一體適用
    result =request.session.items()
    newlist=""
    for key,value in result:
          newlist=newlist+key+" : "+value+"<br>"
          
    return HttpResponse(newlist)

def del_session(request,key=None):
    if key in request.session:
        #跟設值一樣,都是用字典方式來執行,只是這裡是刪值,所以要用del
        del request.session[key]
        return HttpResponse(key +"was deleted!!")
    else:
        return HttpResponse("no session "+key)
from django.contrib.auth import authenticate
from django.contrib import auth

def login_backup(request):
    cursor=connections["default"].cursor()
    sql ="select * from myapp_webuser  "
    cursor.execute(sql,[])
    result=cursor.fetchall()
    newlist=[]
    field_name=cursor.description
    for data in result:
        i=0
        dict_data={}
        for d in data:
            dict_data[field_name[i][0]]=d
            i=i+1
        newlist.append(dict_data)
    #for dic in newlist:
       # print(dic["username"])

    if request.method == "POST":
        username =request.POST["username"]
        password=request.POST["password"]
        for dic in newlist:

            if username in dic["username"]:
                status ="login"
                message=username+"  logged!!"
                request.session["username"]=username
                
        return HttpResponse(message)
    else:
        return render(request,"login.html",locals())


def login(request):
    #進函式先取得資料庫所有資料
    cursor=connections["default"].cursor()
    sql ="select * from myapp_webuser  "
    cursor.execute(sql,[])
    result=cursor.fetchall()
    newlist=[]
    field_name=cursor.description
    for data in result:
        i=0
        dict_data={}
        for d in data:
            dict_data[field_name[i][0]]=d
            i=i+1
        newlist.append(dict_data)
  #===================我是分隔線==============
    

    if request.method == "POST":
        #POST值先拿到,避免2次作業
        username =request.POST["username"]
        password=request.POST["password"]
        #假若username的session不存在,則建立,已存在則判斷動作
        if  not "username" in request.session:
            
            for dic in newlist:

                if username in dic["username"]:
                    status ="login"
                    message=username+"  logged!!"
                    request.session["username"]=username
                #用這種只傳特定變數的方法比較安全

                    context={"status":"login","message":username+"  logged!!"}
            return render(request,"login.html",context)
                    
           # return render(request,"login.html",locals())
        else:
            #當session存在,就去驗證session值是不是符合資料庫內的值
            for dic in newlist:

                if request.session["username"]  in dic["username"]:
                    status ="login"
                    message=request.session["username"] +" session existed!!"
            return render(request,"login.html",locals())
                    
            

    else:
        return render(request,"login.html",locals())



    return render(request,"index.html",locals())
from django.contrib.auth import authenticate
from django.contrib import auth
def login2_backup(request):
    #目前這個authenticate沒辦法正常運件,還找不到原因
    if request.method =="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/index")
        else:
            message="帳號密碼錯誤"
            return render(request,"login.html",locals())
    return render(request,"login.html",locals())
#以下開始,是利用django功能建立基本驗證及登錄頁面,非常快速
#而且這個機制下的都是要建立在/accounts/下
from django.contrib.auth.decorators import login_required




#登入
from .forms import LoginForm
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #仿照這個方式去改原本不作用的部份
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #下面這個只接受一個參數
            login(request)
            return redirect('/accounts/index')  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, 'login_django.html', context)

# 登出
def log_out_django(request):
    logout(request)#只會對當前頁面logout
    auth.logout(request)  # 登出管理員,也就是admin頁面
    return redirect('/accounts/login') #重新導向到登入畫面




# 註冊2  使用RegisterForm()表格,這個類別已經在myapp底下的forms.py定義了
from .forms import RegisterForm
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/index')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'register_django.html', context)
#註冊1 這個UserCreationForm畫面很醜,也不是一般使用的
from django.contrib.auth.forms import UserCreationForm
def sign_up_backup(request):
    #這裡的form就是變數,接了要套用的表格方法後再丟過去html頁面
    form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'register_django.html', context)


#上面的語法是加一項機制,可以強制在使用下面函式之前有前置動作要完成
def index_django(request):
    return render(request, 'index_django.html')

#接下來要測試驗證後的index畫面

from django.contrib.auth import authenticate
from django.contrib import auth
def login2(request):
    #目前這個authenticate沒辦法正常運件,還找不到原因
    if request.method =="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            status="login"
            message="歡迎"+username+"!!"
            return render(request,"login.html",locals())
        else:
            message="帳號密碼錯誤"
            return render(request,"login.html",locals())
        
#登入後轉回主頁
def login3(request):
    #authenticate要運作的條件是密碼要是加密的 
    #這裡可以再加設定,讓已經login的人再回到login畫面時是直接跳回主頁,並且提示已經login了
    #只有還沒登入的人可以看到登入畫面
    if request.method =="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            
            auth.login(request,user)
            status="login"
            message="歡迎"+username+"!!"
            return render(request,"index.html",locals())
        else:
            #下面的手法是利用ORM的功能，而且用.exists()方法找辨證
            user_exists = webUser.objects.filter(username=username).exists()
            if user_exists:
                message = "密碼錯誤"
            else:
                message = "帳號不存在"
            return render(request, "login.html", locals())
                    
    else:
        return  render(request,"login.html",locals())

from django.contrib.auth import authenticate
from django.contrib import auth
def logout(request):
    if "username" in request.session:
        message =request.session["username"]+ "您已登出!"
        status="logout"
        del request.session["username"]
        logout(request)#只會對當前頁面logout,也就是清session
        auth.logout(request)  # 登出管理員,也就是admin頁面
        return render(request,"index.html",locals())
    else:
        
         status="logout"
         auth.logout(request)  # 登出管理員,也就是admin頁面,這個才會清掉authenticate
         return render(request,"index.html",locals())

def test(request):
    if request.user.is_authenticated:
        message="u have permission to login"
        return render(request,"test.html",locals())
    
    else:
        message="no permission to login"

        return render(request,"test.html",locals())


def webuser_admin_backup(request):
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
#目前可以區分使用者來撈取不同的資訊
def webuser_admin(request):
    #當有獲得驗證時
    if request.user.is_authenticated:
        #get all data from model of webuser first
        #pick all vlaues to del_page
        cursor = connections["default"].cursor()
        #分辨一下是一般使用者還是admin
        if request.user.is_superuser:
        # 使用者具有管理權限
        # 執行全部的查詢
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

        else:
            # 執行指定id的查詢
            #用下列的方式來取得實際的id
            user=request.user.id
            sql =" select * from myapp_webuser where id = '%s' "
            sql %=(user)
            cursor.execute(sql,[])
            result =cursor.fetchall()
            field_names =cursor.description
            user_list=[]
            for data in result:
                i=0
                dict_data={}
                for d in data:
                    dict_data[field_names[i][0]]=d
                    i=i+1
                user_list.append(dict_data)

            return render(request,"webuser_admin.html",locals())
     
    else:
        return redirect("/login3")
    
     
        
        
    
        
from datetime import date
#新增一個哈希法的密碼生成
from django.contrib.auth.hashers import make_password
def vip_user_add_backup(request):
    #這裡可以設定依權限來建立不同的使用者,超級使用者建立出來的,都是管理者,管理者只能建立一般使用者

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
             hashpasswd =make_password(password)
        
             cursor=connections["default"].cursor()


             sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
             sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
             sql %= (username_input,hashpasswd,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

             cursor.execute(sql,[])
            except:
             return HttpResponse("account existed!!")
        return redirect("/login3")

    else:
        return HttpResponse("Plz use Post method to input ur data")
    

from datetime import date
#新增一個哈希法的密碼生成
from django.contrib.auth.hashers import make_password
def vip_user_add(request):
    #這裡可以設定依權限來建立不同的使用者,超級使用者建立出來的,都是管理者,管理者只能建立一般使用者
    if request.user.is_authenticated:
       if request.user.is_superuser:
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
                    superuser=request.POST.get("superuser")
                    staff=request.POST.get("staff")
                    active=1
                    hashpasswd =make_password(password)
                
                    cursor=connections["default"].cursor()


                    sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
                    sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
                    sql %= (username_input,hashpasswd,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

                    cursor.execute(sql,[])
                except:
                 return HttpResponse("account existed!!")
            return redirect("/login3")
       elif request.user.is_staff:
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
                    staff=request.POST.get("staff")
                    active=1
                    hashpasswd =make_password(password)
                
                    cursor=connections["default"].cursor()


                    sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
                    sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
                    sql %= (username_input,hashpasswd,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

                    cursor.execute(sql,[])
                except:
                 return HttpResponse("account existed!!")
            return redirect("/login3")
       else:
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
                    hashpasswd =make_password(password)
                
                    cursor=connections["default"].cursor()


                    sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
                    sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
                    sql %= (username_input,hashpasswd,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

                    cursor.execute(sql,[])
                except:
                 return HttpResponse("account existed!!")
            return redirect("/login3")
           
    else:
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
                    hashpasswd =make_password(password)
                
                    cursor=connections["default"].cursor()


                    sql="insert into myapp_webuser(username,password,phone,addr,hobit,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,join_date)"
                    sql += " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now()) "
                    sql %= (username_input,hashpasswd,phone,addr,hobit,superuser,first_name,last_name,email,staff,active)

                    cursor.execute(sql,[])
                except:
                 return HttpResponse("account existed!!")
            return redirect("/login3")

        else:
            return HttpResponse("Plz use Post method to input ur data")


from .forms import productForm
#主要應該還是.files的功能來執行IMAGE檔案的對導
def upload_product_ORM(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form =productForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            return redirect("/upload_show")
        else:
            form=productForm()
            context={"form":form}
            return render(request,"upload_test.html",context)
            
       
    else:
        return HttpResponse("no permission")
from .forms import productForm
import sys
from urllib.parse import quote
def upload_product(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # 連結資料庫
            cursor = connections["default"].cursor()

            form_data = request.POST.dict()
            file_data = request.FILES.dict()

            # 轉換字串編碼
            if sys.stdout.encoding != 'UTF-8':
                form_data = {k: v.encode('utf-8') if isinstance(v, str) else v for k, v in form_data.items()}
                file_data = {k: v.encode('utf-8') if isinstance(v, str) else v for k, v in file_data.items()}

            # 插入資料到 product 資料表
            sql = """
            INSERT INTO myapp_product (item_name, item_description, item_price, item_photo_image)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                    form_data['item_name'],
                    form_data['item_description'],
                    form_data['item_price'],
                    file_data['item_photo_image'].read()  # 讀取圖片的二進制數據
                )


            cursor.execute(sql, values)

            return redirect("/upload_show")

        else:
            form = productForm()
            context = {"form": form}
            return render(request, "upload_test.html", context)
    else:
        return HttpResponse("no permission")
    

from .models import product
def upload_product_sql(request):
    if request.user.is_authenticated:
        if request.method == "POST":
           prod =product()
           prod.item_name =request.POST.get('item_name')
           prod.item_description =request.POST.get('item_description')
           prod.item_price =request.POST.get('item_price')
           if len(request.FILES) != 0:
                prod.item_photo_image =request.FILES["item_photo_image"]
           prod.save()
         
          


           return redirect("/upload_show")

        else:
           
            return render(request, "upload_post.html")
    else:
        return HttpResponse("no permission")
from .models import product
def upload_show(request):
    pro = product.objects.all()
    context = {
        'product': pro
    }
    print(pro)
    return render(request, 'upload_show.html', context)
from .models import shopitem
def get_shopitem(request):
    if request.user.is_authenticated:
        user = request.user # 先通過驗證,再取得user物件,這時的user物件是以webUser模型為主的
        #因為一路用ForeignKey跟隨,所以最後follow的是webUser的主鍵,也就是id
        #
        item_list = []  # List to store the item values
        items = shopitem.objects.filter(item_id=user.id) #中間可以省略很多，反正就是將webUser裡的id屬性代入shopitem的item_id屬性,找到對應值
        print(items)
        for item in items:
            
            item_name = item.item_name.item_name
            item_description = item.item_name.item_description
            item_price = item.item_name.item_price
            item_photo_image=item.item_name.item_photo_image
            # Create a dictionary to store the item values
            item_dict = {
                'item_name': item_name,
                'item_description': item_description,
                'item_price': item_price,
                'item_photo_image': item_photo_image
            }
            item_list.append(item_dict)
        return render(request,"shop_item.html",locals())
#下面的方式可以用SQL來呈現圖片
import os
from django.conf import settings
def product_buy(request):
    if request.user.is_authenticated:
        cursor=connections["default"].cursor()
        sql ="select * from myapp_product  "
        cursor.execute(sql,[])
        result= cursor.fetchall()
        field_names=cursor.description
        product_list=[]
        
        for data in result:
            dict_data={}
            i=0
            for d in data:
                dict_data[field_names[i][0]]=d
                i=i+1
            product_list.append(dict_data)
             # 組合圖片路徑,看來是路徑的問題
            media_path = os.path.join(settings.MEDIA_URL, dict_data['item_photo_image'])
            dict_data['item_photo_path'] = media_path
       
        print(product_list)
        return render(request,"product_buy.html",locals())
    else:
        return HttpResponse("no permission")
    
def buy_select(request,id=None):
    
    item_id =id
    if request.method == "GET":
       
        cursor=connections["default"].cursor()
        sql = "select * from myapp_product  where productid = '%s' "
        sql %= (item_id)
        cursor.execute(sql,[])
        field_name =cursor.description
        result=cursor.fetchall()
        
        
        for data in result:
            pro_select={}
            i=0
            for d in data:
                pro_select[field_name[i][0]]=d
                i=i+1
            #直接引用圖片路徑會認不得,必須用下面的方式帶入才行,不然就要用ORM
            media_path = os.path.join(settings.MEDIA_URL, pro_select['item_photo_image'])
            pro_select['item_photo_path'] = media_path
            print(pro_select)
  
        return render(request,"buy_select.html",{"pro_select":pro_select})
    else:
        return HttpResponse("wrong method")
    
    
def shopcar_add(request):
    if request.method == "POST":
        #進來要先確認shopcar 在不在,不在的話,就生成
        #先取得userid
        userid =request.user.id#這是webUser的主鍵
        #再取得POST過來的資訊
        quantity=request.POST["quantity"]
        item_id=request.POST["item_id"]#這是product的主鍵
        price =request.POST["price"]#這是傳過來的product的價格
     
        cursor=connections["default"].cursor()
        #這裡是用外鍵去連結webUser的id,所以要用carid_id才會找到對的資料
        #簡單說,就是在找特定的webUser下的shopcar
        sql =" select * from myapp_shopcar where carid_id = '%s' "
        sql %= (userid)
        cursor.execute(sql,[])
        result =cursor.fetchall()

        if  not result :
                #當沒有資料時,要創建一筆資料給shopcar,同時將資料增至shopitem
                #這裡的shopcar裡的carid用外鍵去關聯webUser的id 所以用carid_id,但生成後會有新的shopcar主鍵
                #簡言之，用webUser特定用戶為值去輸入到shopcar,這是關聯式的用法
                sql_shopcar="insert into myapp_shopcar (carid_id) "
                sql_shopcar +="values ('%s')"
                sql_shopcar %= (userid)
                cursor.execute(sql_shopcar,[])
                #新增完購物車以後,新增shopitem
                
                # 获取插入的购物车记录的主键值
                #shopitem的item_id對應的是shopcar的主鍵,所以應該是要用shopcar的主鍵,而carid非主鍵,只是這是個FK鍵而已
                shopcar_id = cursor.lastrowid
                #完成輸入後,要重新抓取對應的product的欄位值
                  # 获取商品的信息
                product_sql = "SELECT item_description, item_price, item_photo_image FROM myapp_product WHERE productid = %s"
                cursor.execute(product_sql, [item_id])
                product_data = cursor.fetchone()
             
                item_description = product_data[0]
                item_price = product_data[1]
                item_image_photo = product_data[2]
                #抓取完後,一併新增入資料
                #另外,item_sum要等於item_price 乘以 item_quantity
                #這裡的設定要轉型態是因為html用type=number送過來好像不確定會判斷成什麼型態的數字,所以還是要轉?
                item_sum =item_price * int(quantity)
                #執行shopitem新增,這是完全沒有的時候的新增狀況
                sql_shopitem = "INSERT INTO myapp_shopitem (item_id_id,item_quantity,item_name_id,item_price,item_sum )  "
                sql_shopitem += " VALUES ('%s','%s','%s','%s','%s')"
                sql_shopitem %= (shopcar_id,quantity,item_id,item_price,item_sum)
                try:
                    cursor.execute(sql_shopitem, [])
                   
                except Exception as e:
                    print("插入数据时发生错误:", str(e))
                #執行fetchone()或fetchall()之前都要執行select語句,不然會沒有返回資料可以抓
                #這裡的抓值應該還好,因為是找對應的購物車裡的商品,現在只會有一筆新的,所以不用特別再索引購物車商品id
                #當購物車存在時，就要用這個方式先抓出對應的商品索引id,等等如果要修改時，就是要靠購物車id跟商品欄id來抓
                cursor.execute("SELECT * FROM myapp_shopitem WHERE item_id_id = %s", [shopcar_id])
                shopitem_get = cursor.fetchone()
                field_name =cursor.description
                dict={}
                i=0
                for d in shopitem_get:
                    dict[field_name[i][0]]=d
                    i=i+1
                print("新的購物清單",dict)
                #再來要新增shopsum,關聯是跟shopcar,也是要抓取新的shopsum的pk值.也就是shopcar_id
                insert_sum_sql =" insert into myapp_shopsum ( sum_id_id ,shop_Totalsum) "
                insert_sum_sql += " values ('%s','%s') "
                sum_Total=0
                sum_Total += item_sum
                insert_sum_sql %= (shopcar_id,sum_Total)
                #這樣就新增了shop_sum
                cursor.execute(insert_sum_sql,[])
               
                return HttpResponse(" shopcar and shopitem added!!")
        else:
            # 有購物車,必定有shopsum,因為在之前的判斷式已經新增了,但shopitem只是可能用
            #這裡要先處理的就是當shopitem存在時，要避免因重複而造成的錯誤,要改用update
            #先找到購物車的pk鍵值
            sql_shopcar_check = "SELECT id FROM myapp_shopcar WHERE carid_id = %s"
            cursor.execute(sql_shopcar_check, [userid]) 
            result_shopcar = cursor.fetchone()
            #先撈shopcar主鍵出來
            shopcar_id = result_shopcar[0] 
            print("======== result=======")
            print(result_shopcar)
            # 获取商品的信息,因為現有的shopitem模組裡的資訊不夠?似乎是
            product_sql = "SELECT item_description, item_price, item_photo_image,item_name FROM myapp_product WHERE productid = %s"
            cursor.execute(product_sql, [item_id])
            product_data = cursor.fetchone()
            item_description = product_data[0]
            item_price = product_data[1]
            item_image_photo = product_data[2]
            product_name=product_data[3]
            #查找已存在的shopitem ,要用shopcar跟product雙關聯當關鍵索引去找,才能找到對的shopitem
            #這裡的item_id是藉由前端傳過來的productid 這裡的shopcar_id是新增後的shopcar的主鍵
            shopitem_exsit_sql =" select * from myapp_shopitem where item_id_id='%s' and item_name_id='%s' "
            shopitem_exsit_sql %=(shopcar_id,item_id)
            #執行sql語法,確認有無返回shopitem物件,這時返回的應該也是一個tuple
            cursor.execute(shopitem_exsit_sql,[])
            #返回物件
            shopitem_exsit=cursor.fetchone()
            #這裡要區分shopitem有沒有存在，意思就是,新增不同類的商品要有不同的判斷
            if not shopitem_exsit:
                     #當商品欄沒有的時候，表示有不同的商品正在輸入，所以要做的是將這筆商品新增,並將新增的值加入shopsum
                    #新增不同的商品時,只要在同一個購物車就好
                    #所以要先找目前對應的購物車,藉由外鍵carid 關聯式carid_id  去對應webUser的主鍵值
                    current_shopcar_sql ="select id from myapp_shopcar where carid_id='%s' "
                    current_shopcar_sql %=(userid)#userid是webUser的主鍵值
                    cursor.execute(current_shopcar_sql,[])
                    find =cursor.fetchone()
                    current_carid =find[0]#拿到shopcar的主鍵了,再來要拿product的主鍵
                    #拿product的主鍵 ,在上面有用item_id去拿到POST的資料,再來要拿新的quantity數量,在上面也拿到POST的資料了
                    #price也在上面獲得了,只有item_sum要重新計算
                    current_sum =int(quantity)*int(price)
                    #該有的參數都有了,就可以執行新增了                
                    shopitem_insert_sql ="insert into myapp_shopitem (item_id_id,item_name_id,item_quantity,item_price,item_sum)   "
                    shopitem_insert_sql += " values('%s','%s','%s','%s','%s')"
                    shopitem_insert_sql %=(current_carid,item_id,quantity,price,current_sum)
                    cursor.execute(shopitem_insert_sql,[])
                    #重點來了,這裡新增完以後,要重新獲得這個shopitem的主鍵,這樣才能在後續操作時,不會更新錯商品欄
                    #這裡查找時，不止要找對shopcar也要找對product的主鍵,才會找到對應的資料
                    shopitem_reget_sql ="select  id from myapp_shopitem where item_id_id='%s' and item_name_id ='%s' "
                    shopitem_reget_sql %=(shopcar_id,item_id)
                    cursor.execute(shopitem_reget_sql,[])
                    find_shopitem=cursor.fetchone()
                    new_shopitem_id=find_shopitem[0]#找到新的shopitem的主鍵
                    #新增沒問題，但是要再執行shopsum的更新,由於是新增,所以不需要將總和扣掉現有值,直接將新增的shopitem現有值加入就好
                    #撈取目前的總和,當然還是要用外鍵對應的shopcar來使用,也就是shopcar_id,
                    current_shopsum_sql ="select shop_Totalsum from myapp_shopsum where sum_id_id ='%s' "
                    current_shopsum_sql %= (shopcar_id)
                    cursor.execute(current_shopsum_sql,[])
                    current_shopcar =cursor.fetchone()
                    print(current_shopcar,"before current_shopcar")
                    current_Totalsum=current_shopcar[0]
                    print("current_Totalsum",current_Totalsum)
                    current_Totalsum += current_sum
                    #重新將值更新回shopsum裡
                    #第一種寫法,直接練用語法重新放回資料,這寫法不行,應該是哪裡有問題
                    # current_shopcar=(current_Totalsum,)
                    # print(current_shopcar,"current_shopcar")
                    #第二種寫法,重新用sql語法放回
                    update_shopsum_sql =" update myapp_shopsum set shop_Totalsum='%s' "
                    update_shopsum_sql += "where sum_id_id='%s' "
                    update_shopsum_sql %= (current_Totalsum,shopcar_id)
                    cursor.execute(update_shopsum_sql,[])
                    return HttpResponse("新增不同商品")
            else:

                #由於下面的式子需要新的quantity,所以這裡應該要獲得才對,因為現在獲得的值沒有一個適當的索引,所以還是要用欄位重新定位
                field_shopitem =cursor.description
                shopitem_dict={}
                i=0
                for data in shopitem_exsit:
                    
                    
                    shopitem_dict[field_shopitem[i][0]]=data
                    i=i+1

                if shopitem_exsit:
                    #當商品欄有存在時的處理,表示有同樣的商品正在輸入,所以要做的是更改這個商品的quantity重新update
                    #並且要將原有的shopsum內的總和扣掉原有的商品item_sum,重新以現有的item_sum再加入shopsum
                    #將上面的shopitem_dict的quantity值取出來
                    print("shopitem_dict",shopitem_dict)
                    current_quantity=shopitem_dict["item_quantity"]
                
                    current_itemsum =shopitem_dict["item_sum"]#這個是要先扣掉的
                    
                    #在處理新的輸入值動作前,要先將現有的shopsum的總和先扣掉
                    #抓取現在的總和,關聯也是shopcar ,所以用目前抓到的shopcar主鍵shopcar_id索引
                    shopsum_total_get ="select * from  myapp_shopsum where sum_id_id ='%s' "
                    shopsum_total_get %= (shopcar_id)
                    cursor.execute(shopsum_total_get,[])
                    current_sumTotal =cursor.fetchone()
                    field_sum =cursor.description
                    dict_shopsum={}
                    i=0
                
                    for data in current_sumTotal:
                        
                        dict_shopsum[field_sum[i][0]]=data
                        i=i+1
                    current_Totalsum=dict_shopsum["shop_Totalsum"]#抓到現有的總和
                    
                    current_Totalsum -= current_itemsum#減掉目前的小計
                
                    dict_shopsum["shop_Totalsum"]=current_Totalsum#再重新放到總和去

                    print("在還沒處理前的current_Totalsum",current_Totalsum)
                    print("在還沒處理前的current_itemsum",current_itemsum)
                    
                    #接下來針對更改的部份去update
                    #先更新shopitem ,這裡要把新輸入的quantity代入,也就是request.POST獲得的部份
                    #這裡重新代入的item_sum應該要計算前端送過來的quantity跟product裡的price相乘的結果
                    #這裡的item_price是透過POST截取傳來的產品價格
                    #但前端傳來的資訊要透過int轉型才能用,不然的話,不是後端可以處理的數值型態
                    current_itemsum=int(quantity) *item_price
                    shopitem_update_sql ="update myapp_shopitem  set item_quantity='%s' ,item_sum ='%s'"
                    shopitem_update_sql += " where item_id_id='%s' and item_name_id='%s'  "
                    shopitem_update_sql %=(quantity,current_itemsum,shopcar_id,item_id)
                    cursor.execute(shopitem_update_sql,[])
                    #我們需要重新獲得的小計,所以要再查找一次shopitem
                    #檢查一下進總和前的變數是不是對的
                    print("current_Totalsum",current_Totalsum)
                    print("current_itemsum",current_itemsum)
                    shopitem_repost_sql="select item_sum from myapp_shopitem " 
                    shopitem_repost_sql +=" where item_id_id='%s' and item_name_id='%s' "
                    shopitem_repost_sql %=(shopcar_id,item_id)
                    cursor.execute(shopitem_repost_sql,[])
                    shopitem_new =cursor.fetchone()
                    shopitem_sum =shopitem_new[0]
                    print("shopitem_sum",shopitem_sum)
                    #再來是修訂shopsum，在執行之前記得先把item_sum先扣掉，我們上面的式子已經處理完扣掉的部份了.
                    #接下來就是處理新增的部份,由於新增需要有新的item_sum小計,所要要記得重新抓
                    current_Totalsum +=shopitem_sum# 將新的小計重新加到總和裡
                    update_shopsum_sql =" update myapp_shopsum  set  shop_Totalsum ='%s'  "
                    update_shopsum_sql += " where sum_id_id='%s' "
                    update_shopsum_sql %=(current_Totalsum,shopcar_id)
                    cursor.execute(update_shopsum_sql,[])

                    
                    print("=====update原有商品====")
                    return HttpResponse("update原有商品")
                else:
                   
                    
                  
                    return HttpResponse("商品不存在!!")
                
            


            #所以重新修正數字可能會出錯，因為可能改到同樣購物車裡的其他商品資訊
            #目前是以單一商品來修改，所以暫時還不會出錯，可以順利完成資料修訂

            # if result_shopcar:
            #     shopcar_id = result_shopcar[0]  # 获取shopcar的主键值
            #     #有購物車,要先判斷原來的shopitem的id是不是重複，也就是輸入的值item_name有沒有重複,item_name是fk對product,
            #     #所以要先用product的主鍵來對應目前的shopitem裡的item_name_id有沒有值

            #     #當購物車存在時，有哪些狀況?shopitem跟shopsum這時都會有值?不一定，因為第1次進判斷式時，shopsum可能還不存在
            #     #所以我們要在這裡先判斷shopsum存不存在，用shopcar當索引值去找,把需要欄位都找出來
            #     search_shopsum =" select   id,shop_Totalsum  from myapp_shopsum where  sum_id_id ='%s' "
            #     search_shopsum %=(shopcar_id)
            #     #執行SQL語法
            #     cursor.execute(search_shopsum,[])
            #     #先確定物件有沒有存在
            #     shopsum_exist =cursor.fetchone()
            #     if shopsum_exist:
            #         return HttpResponse("總和欄位已存在!!!")
            #     else:
            #         #不存在就新增shopsum,要用shopcar去對應
            #         shopsum_add_sql=" insert into myapp_shopsum set  (shop_Totalsum) "
            #         shopsum_add_sql += " values ('%s') where sum_id_id ='%s' "
            #         shopsum_add_sql %=("",shopcar_id)



               
                

            #     #目前這裡的search方式可能有問題,只指定了購物車,但是沒有指定shopitem的id
            #     #要怎麼找到對應的shopitem的id? 可以用購物車+商品的id去找,就可以找到特定的shopitem的id!!!
            #     shopitem_name_search="select * from myapp_shopitem where item_id_id ='%s' "
            #     shopitem_name_search %=(shopcar_id)
            #     cursor.execute(shopitem_name_search,[])
            #     #有購物車的情況下,應該要用fetchall()才能找到所有資料
            #     shopitem_get =cursor.fetchall()
            #     field_name =cursor.description
            #     new_list=[]
            #     for data in shopitem_get:
            #         dict={}
            #         i=0
            #         for d in data:
            #             dict[field_name[i][0]]=d
            #             i=i+1
            #         new_list.append(dict)
            #     print("購物車存在的情況下,找到的shopitem的字典",dict)
            #     print("當購物車存在的情況下,找到的shopitem內資料",new_list)
            #     #但有購物車的情況下，不見得只會有一筆商品,所以目前的都會取到第1組商品，這不對
            #     #所以不能只對購物車的id,也要對product的id,這樣找到的shopitem才會是目標值
            #     shopid=shopitem_get[0][5]
            #       #這裡的設定要轉型態是因為html用type=number送過來好像不確定會判斷成什麼型態的數字,所以還是要轉?
            #     item_sum =item_price * int(quantity)
            #     #判斷shopitem有沒有存在,有就update,沒有就insert into
            #     print("item_id",item_id)
            #     print("shopid",shopid)
            #     #沒有轉型會判斷錯誤,可能因為item_id是用html送過來的,可能都要轉型才會正確
            #     if int(item_id) == shopid:
            #         #不對,現有的式子是當目前的購物車相同的情況下
            #         shopitem_update ="update myapp_shopitem set item_quantity='%s',item_price='%s',item_sum='%s' "
            #         shopitem_update += "where item_id_id='%s' and item_name_id='%s' "
            #         shopitem_update %= (quantity,item_price,item_sum,shopcar_id,item_id)
            #         cursor.execute(shopitem_update,[])
            #         #這裡應該要新增至shopsum加總,不然會出錯,但因為是更換了原有的item 數量,所以理論上要把總和清掉重撈?不行,因為會有其他組的shopitem,但不清掉的話會出錯
            #         #所以要在執行新的指令之前，先把現有對應的shopitem_sum撈出來扣掉,where的位置要指定shopcar 跟product(因為這個不重複)

            #         #也就是要重新撈現有的shopitem的item_sum 
            #         #要加總的話，因為已經有新的shopsum,所以只用關聯的外鍵shopcar_id進去撈shopsum有沒有對應的id鍵,然後用這組id鍵update
            #         shopsum_id_search_sql ="select id,shop_Totalsum from myapp_shopsum where sum_id_id = '%s' "
            #         shopsum_id_search_sql %=(shopcar_id)
            #         cursor.execute(shopsum_id_search_sql,[])
            #         current_shopsumid_dict =cursor.fetchone()
            #         current_shopsumid=current_shopsumid_dict[0]#找到id
            #         current_Totalsum=current_shopsumid_dict[1]#找到Totalsum
            #         #我也要找到現在shopitem裡的item_sum
            #         shopitem_sumsearch_sql=" select id,item_sum  from myapp_shopitem where item_id_id='%s' and item_name_id='%s' "
            #         shopitem_sumsearch_sql %= (shopcar_id,item_id )
            #         cursor.execute(shopitem_sumsearch_sql,[])
            #         current_shopitem =cursor.fetchone()
            #         current_shopitem_id=current_shopitem[0]
            #         current_shopitem_sum=current_shopitem[1]

            #         shopsum_update_sql ="update myapp_shopsum set shop_Totalsum='%s'  where id ='%s' "
            #         current_Totalsum += current_shopitem_sum
            #         shopsum_update_sql %=(current_Totalsum,current_shopitem_id)
            #         cursor.execute(shopsum_update_sql,[])



            #         return HttpResponse("shopitem existed and updated!!")
            #     else:
            #         sql_shopitem = "INSERT INTO myapp_shopitem (item_id_id,item_quantity,item_name_id,item_price,item_sum )  "
            #         sql_shopitem += " VALUES ('%s','%s','%s','%s','%s')"
            #         sql_shopitem %= (shopcar_id,quantity,item_id,item_price,item_sum)
            #         cursor.execute(sql_shopitem, [])
            #         #再來要新增shopsum,關聯是跟shopcar,也是要抓取新的shopsum的pk值.也就是shopcar_id
            #         #理論上,若已經有購物車,表示有一個唯一的shopsum存在,必須有判斷式判斷若shopsum存在,則使用update
            #         sumTotal_id_search =" select id , shop_Totalsum from myapp_shopsum where sum_id_id = '%s' "
            #         sumTotal_id_search %=(shopcar_id)
            #         cursor.execute(sumTotal_id_search,[])
            #         sum_result =cursor.fetchone()
                   
            #         if sum_result:        
            #             update_sum_sql =" update myapp_shopsum SET  shop_Totalsum ='%s' where sum_id_id='%s' "
                        
            #             sum_Total=sum_result[1]#找到已存在的總和
                        
            #             sum_Total += item_sum
            #             update_sum_sql %= (sum_Total,shopcar_id)
            #             cursor.execute(update_sum_sql,[])

            #             return HttpResponse("new shopitem  added and shopsum updated!!")
            #         else:
            #             return HttpResponse("new shopitem  added and shopsum not updated!!")

    else:

        return HttpResponse("wrong method")
   


               
               
from django.db import connection
from .models import shopcar, shopitem
#購物車顯示
def shopcar_show(request):
    #這裡要去抓shopitem裡的資料
    #當然啦,一開始要驗證有沒有權限
    if request.user.is_authenticated:
        #抓資料
        #連結資料庫
        cursor=connections["default"].cursor()
        #先找shopcar當時的id,用關聯式的webUser主鍵去找
        sql_shopcar_search ="select id from myapp_shopcar where carid_id ='%s' "
        carid=request.user.id#這裡已經找到webUser的主鍵
        sql_shopcar_search %= (carid)
        cursor.execute(sql_shopcar_search,[])
        result_carid =cursor.fetchone()
        current_carid=result_carid[0]#這裡獲得的是shopcar的主鍵
        #把找到的carid 當成搜尋條件
        sql_shopitem_get ="select * from myapp_shopitem where item_id_id ='%s' "
        sql_shopitem_get %=(current_carid)
        cursor.execute(sql_shopitem_get,[])
        current_shopitems=cursor.fetchall()
        field_name=cursor.description
        #放到新的list
        print("===查看目前資料===")
     
     
        new_shopitem_list=[]
        for data in current_shopitems:
            item={}
            i=0
            #應該在這個位置獲得item_name_id的值,再去找對應的product
            productid =data[5]#獲得不同的productid
            #執行sql語法查詢
            current_product_sql =" select * from myapp_product where productid='%s' "
            current_product_sql %=(productid)
            cursor.execute(current_product_sql,[])
            product_list=cursor.fetchall()
           # print("product_list",product_list)#到這裡為止是雙層tuple
            product_num=product_list[0][0]
            product_name=product_list[0][1]
            product_description=product_list[0][2]
            product_price =product_list[0][3]               
            for d  in data:
                item[field_name[i][0]]=d
                i=i+1
                
            item["product_num"]=product_num
            item["product_name"]=product_name
            item["product_description"]=product_description
            item["product_description"]=product_description
            item["product_price"]=product_price
            # #ORM 取值,圖片只能這樣取值
             
            orm_product =product.objects.filter(productid=productid)
            for product_obj in orm_product:
                item_photo_image = product_obj.item_photo_image
                # 将 item_photo_image 放入 item 字典
                item["product_image"] = item_photo_image
            
            

            new_shopitem_list.append(item)
        print(new_shopitem_list,"new_shopitem_list")
           
          
        #    # print(pro)#到這裡就用pro把資料撈出來了
        #     for d in data:
        #         item[field_name[i][0]]=d
        #             # 通过关联属性访问关联的Product对象,用sql就是無法顯示圖片
        #             # 下面的操作要擺在迴圈裡,才會隨著i=i+1 找到不同的商品
        #         product_id =data[1]#第2個位置,找到當時product的主鍵
        #         print(d,"D各元素")
        #         print(product_id,"product_id")
        #         #但目前的資料少了product裡的item_name,所以要從product裡撈出來,而不同的prodcutid要用foreach撈出來
        #         #這裡要反向思考，直接撈

        #         sql_product_search =" select item_name,item_photo_image from myapp_product where productid ='%s'  "
        #         sql_product_search %=(product_id)
        #         cursor.execute(sql_product_search,[])
        #         prod =cursor.fetchone()
        #         pro=prod[0]#這樣才能取乾淨的值
        #         image=prod[1]#取圖片資料
        #         produ = product.objects.get(productid=data[1])
        #         item['pro'] = produ.item_name
        #         item['image'] = produ.item_photo_image
        #         # item["pro"]=pro#存值進dict裡
        #         # item["image"]=image
        #         i=i+1
        #     new_shopitem_list.append(item)
        #     print(new_shopitem_list)
        
        
        
        return render(request,"shopcar_show.html",{"new_shopitem_list":new_shopitem_list})
    else:
        return HttpResponse("no right to access")

def shopitem_action(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            #先連結資料庫,等等可以用
            cursor=connections["default"].cursor()
            #依輸入框的變動,決定要執行什麼動作
            #先獲取目前的輸入值
            input_shopitem_id=request.POST["item_id"]
            print("input_shopitem_id:",input_shopitem_id)
            input_item_name=request.POST["item_name"]
            input_price=request.POST["price"]
            input_quantity=request.POST["quantity"]
            actionType =request.POST["action_type"]
            print(actionType)
            if actionType == "delete":
                shopitem_delete_sql =" delete  from myapp_shopitem where id ='%s' "
                shopitem_delete_sql %=(input_shopitem_id)
                cursor.execute(shopitem_delete_sql,[])
                return redirect("/shopcar_show")


            #要比對的只有quantity的數量,再從原本的shopitem裡撈指定quantity出來
            object =shopitem.objects.filter(item_id=input_shopitem_id)
            print(object)
            #假若值相等,也就是沒有變
            if object[3] == int(input_quantity):
                #當數量相同時,就送出訂單
                return render(request,"shopitem_action.html",locals())
            else:
                #當數量不同時,就修正原有值,update,同理,要更新要先找到對應的shopitem的id 及item_id_id與item_name_id

                update_quantity_sql=" update  from myapp_shopitem set item_quantity ='%s' where id = '%s'  "
                update_quantity_sql %=(input_quantity,input_shopitem_id)
                cursor.execute(update_quantity_sql,[])
                #取回現有的值
                current_shopitem =cursor.fetchon()
                #取欄位名
                field_name = cursor.description
                #重新放值
                new_shopitem_list=[]
                for data in current_shopitem:
                    i=0
                    dict={}
                    for d in data:
                        dict[field_name[i][0]]=d
                        i=i+1
                    new_shopitem_list.append(dict)

                return render(request,"shopcar_show.html",{"new_shopitem_list":new_shopitem_list})
            
            
        else:
            return HttpResponse("wrong method")
        
       
    else:

         return HttpResponse("no permission")
        
