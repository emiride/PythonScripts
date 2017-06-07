import requests
from bs4 import BeautifulSoup
import csv
import lxml
import pandas
from multiprocessing.dummy import Pool as ThreadPool

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

urls = []
start = 2253151
while start > 0:
	urls.append("http://ispovesti.com/ispovest/"+str(start))
	start -= 1
ima = 0
nema = 0
ispovijesti_file = open("ispovijesti.csv", 'w', newline='', encoding='utf-8')
ispovijesti_writer = csv.writer(ispovijesti_file, dialect=csv.excel)
ispovijesti_writer.writerow(["Id","Tekst","Ups","Downs"])

def get_ispovijest(url):
	start = url[url.find("ispovest/")+9:]
	r = requests.get(url, headers = headers)
	page_content = r.content.decode()
	soup = BeautifulSoup(page_content, "lxml")
	try:
		ispovijest = soup.find('div',{'class':'confession-text'}).get_text()
		up = soup.find('div',{'id':'approve-count-'+str(start)}).get_text()
		down = soup.find('div',{'id':'disapprove-count-'+str(start)}).get_text()
		ispovijesti_writer.writerow([start,ispovijest,up,down])
		ispovijesti_file.flush()
		print("Ima: " + str(start))
	except:
		print("Nema: " + str(start))

pool = ThreadPool(200)
results = pool.map(get_ispovijest,urls)

pool.close()
pool.join()
ispovijesti_file.close()