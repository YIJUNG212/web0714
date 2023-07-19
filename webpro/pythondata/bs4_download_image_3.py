import requests,os,urllib.parse

url ='http://aaa.24ht.com.tw/'
response =requests.get(url,allow_redirects=False)
current_url =response.url
print(current_url)