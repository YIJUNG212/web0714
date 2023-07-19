from urllib import parse
url ='http://homepi.myftp.org:8000/product_select/9'
htmlObj =parse.urlparse(url)
print("scheme,URL方案 :",htmlObj.scheme)
print("fragment,片段標示符號: ",htmlObj.fragment)
print("netloc,網路位置: ",htmlObj.netloc)
print("params,最後路徑元素參數: ",htmlObj.params)
print("path,分層路徑: ",htmlObj.path)
print("query",htmlObj.query)




