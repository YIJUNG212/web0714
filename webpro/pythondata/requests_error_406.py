import requests
url = 'https://www.kingstone.com.tw/basic/2014713659590/?lid=search&actid=WISE&kw=python'
htmlfile =requests.get(url)
print(htmlfile.raise_for_status())