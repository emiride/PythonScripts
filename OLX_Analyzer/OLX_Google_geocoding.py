import requests
import json
import pandas as pd
import numpy as np
from threading import Thread
from queue import Queue

KEY = "AIzaSyCEcQX-MJOjDFLS-cPd525gdAAjnY-rfMo"


df = pd.read_csv(r"C:\TaskScheduler\stanovi_24032017.csv")
addresses = df[['Adresa']]
address_list = np.array(addresses)
index_list = np.array(addresses.index.tolist())

lokacija = pd.DataFrame(columns = ['Id','Adresa','Lat','Lng'], index = np.arange(0,len(addresses)))
num = 0
for i in range(len(addresses)):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=Sarajevo,"+str(addresses.Adresa.loc[i])+"&key="+KEY)
    json_string = r.content.decode()
    json_object = json.loads(json_string)
    status = json_object['status']
    if status == 'OK':
        lat = json_object['results'][0]['geometry']['location']['lat']
        lng = json_object['results'][0]['geometry']['location']['lng']
        lokacija.Id.loc[i] = i
        lokacija.Adresa.loc[i] = addresses.Adresa.loc[i]
        lokacija.Lat.loc[i] = lat
        lokacija.Lng.loc[i] = lng
    print(num)
    num += 1
    
lokacija.to_csv(r'C:\Users\emirh\PycharmProjects\OLX_Analyzer\pobjednicki.csv')

