import requests
url ='https://www.httpbin.org/image/jpeg'
r =requests.get(url)
img=r.content
print(img)
print(r.headers.get("content-type"))

# fn ='out3_38.jpg'
# with open(fn,'wb') as fout:
#     fout.write(img)