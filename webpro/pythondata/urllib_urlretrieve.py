import urllib.request
url_pict ='https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
fn ='baidu.png'
pict =urllib.request.urlretrieve(url_pict,fn)