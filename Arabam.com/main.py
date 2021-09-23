import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.testing import db

url = "https://www.arabam.com/ikinci-el/otomobil?take=50"
r = requests.get(url)
r.status_code
r.content
soup = BeautifulSoup(r.content,"lxml")
pages = 50
ilanSayisi = 0
arabaIsim = []
arabaYil = []
arabaKm = []
arabaRenk = []
arabaFiyat = []
arabaIl = []
arabaIlce = []
for pageNumber in range(1, 51):
    pageRequest = requests.get("https://www.arabam.com/ikinci-el/otomobil?take=50&page=" + str(pageNumber))
    print(pageRequest.url)
    pageSource = BeautifulSoup(pageRequest.content,
                               "lxml")  ## döngünün içinde oluşturduğun soup aslında pageSource.find ordan geliyo
    car = pageSource.find_all("tr", attrs={"class": "listing-list-item pr should-hover bg-white"})
    for cars in car:
        print(cars.find("td", attrs={"class": "listing-modelname pr"}).select("h3:nth-of-type(1) > a")[0].text)
        arabaIsim.append(
            cars.find("td", attrs={"class": "listing-modelname pr"}).select("h3:nth-of-type(1) > a")[0].text)

        print(cars.select("td:nth-of-type(4) > div > a")[0].text)
        arabaYil.append(cars.select("td:nth-of-type(4) > div > a")[0].text)

        print(cars.select("td:nth-of-type(5) > div > a")[0].text)
        arabaKm.append(cars.select("td:nth-of-type(5) > div > a")[0].text)

        print(cars.select("td:nth-of-type(6) > div > a")[0].text)
        arabaRenk.append(cars.select("td:nth-of-type(6) > div > a")[0].text)

        print(cars.select("td:nth-of-type(7) > div > span > a")[0].text)
        arabaFiyat.append(cars.select("td:nth-of-type(7) > div > span > a")[0].text)

        print(cars.select("td:nth-of-type(9) > div >div > a > span:nth-of-type(1)")[0].text)
        arabaIl.append(cars.select("td:nth-of-type(9) > div >div > a > span:nth-of-type(1)")[0].text)

        print(cars.select("td:nth-of-type(9) > div >div > a > span:nth-of-type(2)")[0].text)
        arabaIlce.append(cars.select("td:nth-of-type(9) > div >div > a > span:nth-of-type(2)")[0].text)

        ilanSayisi += 1
        print("------------------------------")

print("Toplam İlan Sayisi : " + str(ilanSayisi))

birlesmisarabalistesi =list(zip(arabaYil , arabaKm ,arabaRenk , arabaFiyat ,arabaIl ,arabaIlce) )
birlesmisarabalistesi
carsDataFrame = pd.DataFrame(birlesmisarabalistesi , index = arabaIsim ,columns=["YIL" , "KM" , "RENK" , "FİYAT" , "İL" , "İLÇE"])
carsDataFrame.index.names = ["Araçlar"]
carsDataFrame
Server = '(localdb)\MSSQLLocalDB'   ##Server name
Database = 'Covid19'                  ##SQL TABLO AD
Driver = 'ODBC Driver 17 for SQL Server' ##STANDART
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_Con)
con = engine.connect()

df=pd.read_sql_query("Select * from TBL_Bilgi",con)
df

imlec = db.cursor()
imlec.execute('SELECT * FROM araclistesi')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)
    i = 0
    for i in range(0, ):
        komut = 'INSERT INTO ArabaListesi VALUES(?,?,?,?,?,?,?)'
        veriler = (str(arabaIsim[i]), arabaYil[i], arabaKm[i], arabaRenk[i], arabaFiyat[i], arabaIl[i], arabaIlce[i])
        sonuc = imlec.execute(komut, veriler)
        db.commit()
        i += 1