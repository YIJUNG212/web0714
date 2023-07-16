import requests
url ='https://www.httpbin.org'
r =requests.get(url)
print(r.url)
