import requests
from bs4 import BeautifulSoup
from queue import Queue
import pandas as pd
from time import sleep
import sys, datetime
from itertools import chain
from threading import Thread
import lxml

t = datetime.datetime.now().date()

links = Queue(maxsize=0)
main_list = Queue(maxsize = 0)
urls = Queue(maxsize=0)
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

category = 23 #23-stanovi, 24-kuce, 25-poslovni prostori, 26-vikendice, 30-garaze
from_page = 1
#automatic calculation for number of pages
temp_url = "http://www.olx.ba/pretraga?kategorija=" + str(category) + "&stranica=1&kanton=9"
r = requests.get(temp_url, headers=headers)
page_content = r.content.decode()
soup = BeautifulSoup(page_content, "lxml")

to_page = round(int(soup.find('div',{'class':'brojrezultata'}).find_next('span',{'style':'font-weight:bold'}).get_text().replace('.','').strip())/30 + 1)
print("Number of pages: "+str(to_page))

while from_page < to_page:
    urls.put("http://www.olx.ba/pretraga?kategorija=" + str(category) + "&stranica=" + str(from_page) + "&kanton=9")
    from_page += 1

def page_scraper(urls, file = True):
    if file:
        links_file = open("links.txt", "w")

    print("Number of pages: "+ str(urls.qsize()))
    while not urls.empty():
        try:
            r = requests.get(urls.get(), headers=headers)
            r.raise_for_status()
            page_content = r.content.decode()
            soup = BeautifulSoup(page_content, "lxml")
            articles = soup.find_all(class_="naslov")
            if len(articles) == 0 and r.status_code != 200:

                print("Stopped scraping at page: "+str(from_page))
                return links
            for link in articles:
                links.put(link.a["href"])
                if file:
                    links_file.write("%s\n" % link.a["href"])
            print(links.qsize())
        except:
            sleep(3)
            print("Zasp'o sam sekund... kriv je "+str(r.status_code))
        urls.task_done()
    return links

def car_scraper(q, file = True):
    """
    Scrape info from given links. Use page_scraper for getting links.

    Args:
        q -- preferably a queue, but can accept a list as well
        file -- creates csv file as an output (True is by default)
    Returns:
        Pandas Dataframe consists of all values from given pages
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    while not q.empty():
        attributes = {}
        main_items = {}
        items = {}
        lat = 'NaN'
        lng = 'NaN'
        url = q.get()
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except:
            print("Error: ",sys.exc_info()[0],"  Status code: "+str(r.status_code))
            sleep(3)
            r = requests.get(url, headers=headers)
        page_content = r.content.decode()
        soup = BeautifulSoup(page_content, "lxml")

        main_attrs = soup.find_all('p', {'class': 'n'})
        main_attrs_keys = []
        main_attrs_values = []
        for attr in main_attrs:
            main_attrs_keys.append(attr.get_text().strip())
        for attr in main_attrs:
            main_attrs_values.append(attr.find_next('p').get_text().strip())
        main_items = dict(zip(main_attrs_keys,main_attrs_values))

        df1_list = []
        df2_list = []
        df1 = soup.find_all('div', {'class': 'df1'})
        df2 = soup.find_all('div', {'class': 'df2'})
        for df in df1:
            df1_list.append(df.get_text().strip())
        for df in df2:
            df2_list.append('1' if df.get_text().strip() == '' else df.get_text().strip())
        items = dict(zip(df1_list, df2_list))

        try:
            my_str = soup.find('script',{'src':'//cdnjs.cloudflare.com/ajax/libs/geocomplete/1.4/jquery.geocomplete.min.js'}).next.next.get_text()
            latlng = my_str[my_str.find("google.maps.LatLng(") + 19:]
            latlng = latlng[:latlng.find(")")]
            lat, lng = latlng.split(',')
            lat = lat.strip()
            lng = lng.strip()
        except:
            pass
        geoloc = {'Latitude':lat,'Longitude':lng}
        attributes = {**main_items, **items, **geoloc}
        main_list.put(attributes)
        print(main_list.qsize())
        q.task_done()

    single_list = list(main_list.queue)
    df = pd.DataFrame(single_list)
    if file:
        df.to_csv("stanovi_"+t.strftime('%d%m%Y')+".csv", encoding="utf-8", na_rep="NaN", index=False)
    return df

for i in range(100):
    t1 = Thread(target = page_scraper, args=(urls,))
    t1.start()
urls.join()

for j in range(100):
    t2 = Thread(target = car_scraper, args=(links,))
    t2.start()

links.join()




