import requests,json
headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
         AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/114.0.0.0 Mobile Safari/537.36',}
# url='https://www.httpbin.org/post'
url='https://www.httpbin.org/response-headers?freeform='
form_data={"gender":"M","page":"1"}
r=requests.get(url,headers=headers)
print(r.headers.get("content-type"))
print(r.text)
print(r.json())

# r=requests.post(url,json=form_data,headers=headers)
# print(r.url)
# print("-"*70)
# print('r.request.headers : \n',r.request.headers)
# print("-"*70)
# print('r.headers : \n', r.headers)
# print(r.reason)
# print(r.status_code)
# print(r.encoding)
