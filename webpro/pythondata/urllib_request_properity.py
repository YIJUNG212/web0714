import urllib.request
url ='http://homepi.myftp.org:8000/index'
htmlfile = urllib.request.urlopen(url)
print('版本: ',htmlfile.version)
print('網址: ',htmlfile.geturl())
print('下載: ',htmlfile.status)
print('表頭: ')
for header in htmlfile.getheaders():
    print(header)
