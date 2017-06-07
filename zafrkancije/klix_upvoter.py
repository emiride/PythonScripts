import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {
'Host': 'api.klix.ba',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Accept': '*/*',
'Connection': 'keep-alive',
'Content-Length': '18',
'Origin': 'https://www.klix.ba',
'Referer':'https://www.klix.ba/vijesti/bih/pali-serveri-zbog-kvara-na-rashladnom-sistemu-radi-se-na-popravci/170322075',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.8,hr;q=0.6,bs;q=0.4,sr;q=0.2'
}

rateUp_payload = {
    'sifra':'',
    'type':'rateup'
}
rateDown_payload = {
    'sifra':'',
    'type':'ratedown'
}
url = 'https://api.klix.ba/v1/rate/9782831'

for _ in range(50):
    requests.post(url,data=rateDown_payload,headers=headers, verify=False)
    sleep(2)