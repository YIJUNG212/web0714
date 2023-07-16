import requests
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64)\
        AppleWebKit/537.36 (KHTML,like Gecko) Chrome/45.0.2454.101\
        Safari/537.36',}
url = 'https://www.kingstone.com.tw/basic/2014713659590/?lid=search&actid=WISE&kw=python'
htmlfile =requests.get(url,headers=headers)
print(htmlfile.raise_for_status())
print(htmlfile.text)