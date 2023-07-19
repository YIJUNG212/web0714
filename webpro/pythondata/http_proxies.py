#代理ip

import requests
proxies={
    'https':'http://103.74.147.10:80'
    
}
r=requests.get("http://homepi.myftp.org:8000/index",proxies=proxies)
if r.status_code == 200:
    print('代理IP使用成功')
    # print(r.text)
    print(r.content)