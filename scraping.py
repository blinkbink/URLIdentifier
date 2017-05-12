import requests
request = requests.get('http://www.ganool.com')
if request.status_code == 200:
    print('Web site exists')
else:
    print('Web site does not exist')

#url = 'http://www.delfi.lt/news/daily/medijos-karas-propaganda/jav-gynybos-sekretorius-gerbiu-rusijos-armija-bet-lietuvoje-dislokuosime-tai-ka-reikes.d?id=74600322'
#response = requests.get(url)
#html = response.content

#soup = BeautifulSoup(html)
#text_analyze = (soup.find('title'))
#print (text_analyze)