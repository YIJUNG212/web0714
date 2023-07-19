import urllib.request
url ='http://homepi.myftp.org:8000/index'

headers={'User-Agent':'Mozilla/5.0 \
    (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/114.0.0.0 Mobile Safari/537.36'}

req = urllib.request.Request(url,headers=headers)
html =urllib.request.urlopen(req)

print(html.read().decode('utf-8'))