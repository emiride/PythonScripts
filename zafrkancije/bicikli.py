import requests
from bs4 import BeautifulSoup
from time import sleep
import lxml
import csv

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
url = r"https://www.olx.ba/pretraga?kategorija=22&id=1&stanje=0&vrstapregleda=grid&sort_order=desc&sort_po=datum"
file = open("bicikli.csv", 'w', newline='', encoding='utf-8')
file_writer = csv.writer(file, dialect=csv.excel)
file_reader = csv.reader(file)
file_writer.writerow(["Id"])
temp_bicikli = []
lista = []


def get_first_page_articles():
    r = requests.get(url, headers=headers)
    page_content = r.content.decode();
    soup = BeautifulSoup(page_content, "lxml")
    return soup.find_all('div',{'class':'listitem artikal obicniArtikal imaHover g '})

articles = get_first_page_articles()
while True:
    for article in articles:
        if not article['id'] in temp_bicikli:
            temp_bicikli.append(article['id'])
    sleep(60)
    articles = get_first_page_articles()
    lista = list(file_reader)