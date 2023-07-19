from urllib import parse
ch='中華民國萬萬歲'
urlcode =parse.quote(ch)
print('URL編碼: ',urlcode)

code =parse.unquote(urlcode)
print('轉回中文編碼: ',code)