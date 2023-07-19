import urllib.request
url ='http://homepi.myftp.org:8000/index'
htmlfile = urllib.request.urlopen(url)
print(type(htmlfile))
print(htmlfile)
print(htmlfile.read().decode("utf-8"))