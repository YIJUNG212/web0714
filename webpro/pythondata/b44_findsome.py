import requests,bs4
url='ch5_2_2.html'
htmlFile =open(url,encoding='utf-8')
objSoup =bs4.BeautifulSoup(htmlFile,'lxml')

mycity=[]
cityobj=objSoup.find('dl')
cities =cityobj.find_all('dt')
for city in cities:
    mycity.append(city.text)
mycountry=[]
countryobj=objSoup.find('dl')
countries=countryobj.find_all('dd')
for country in countries:
    mycountry.append(country.text)
data=dict(zip(mycountry,mycity))