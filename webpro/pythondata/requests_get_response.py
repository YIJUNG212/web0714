import requests
url ='http://homepi.myftp.org:8000/index'
htmlfile = requests.get(url)
print(type(htmlfile))
print(htmlfile)