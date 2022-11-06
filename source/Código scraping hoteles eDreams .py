#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Se consulta el archivo robots.txt
from urllib.request import urlopen
with urlopen("https://www.edreams.com/robots.txt") as stream:
    print(stream.read().decode("utf-8"))
# Se comprueba la tecnología usada
import builtwith
print(builtwith.builtwith("https://www.edreams.com/"))
# Se determina quien es el propiertario de la página web
import whois
print(whois.whois("https://www.edreams.com/"))


# In[20]:


# Se importan las librerias necesarias para llevar a cabo el web scraping
import selenium
import requests
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
import time
from selenium.webdriver.common.by import By

# Se establece un user agent de acuerdo a las buenas prácticas y se inicializa el driver
opts=Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36-uoc-student")
driver=webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe", chrome_options=opts)
print(driver.execute_script("return navigator.userAgent"))


# Se accede al enlace donde constan los datos de interés
link="https://hotels.edreams.com/searchresults.es.html?aid=350435&label=edr-link-com-sb-conf-pc-of&sid=dce3e3fb19131ce12c9470a7365079dc&tmpl=searchresults&checkin=2022-11-30;checkout=2022-12-01;class_interval=1;dtdisc=0;fp_referrer_aid=308918;group_adults=1;group_children=0;inac=0;index_postcard=0;label_click=undef;lang=es;no_rooms=1;offset=0;postcard=0;room1=A;sb_price_type=total;shw_aparth=1;si=ai%2Cco%2Cci%2Cre%2Cdi;slp_r_match=0;soz=1;srpvid=cac25a9cd59b0269;ss=barcelona;ss_all=0;ssb=empty;sshis=0&"
driver.implicitly_wait(30)
driver.get(link)
driver.implicitly_wait(10)



# Se crean listas para almacenar los datos a extraer
page=BeautifulSoup(driver.page_source,'html.parser')
titulo_=[]
localizacion_=[]
valoracion_=[]
comentarios_=[]
puntuacion_=[]
distancia_=[]
condiciones_alojamiento_=[]
situacion_=[]
precio_anterior_=[]
precio_actual_=[]

# Se maximiza la ventana y se aceptan las cookies
driver.find_element(By.ID,"onetrust-accept-btn-handler").click()
driver.maximize_window()

# Se extraen los datos de las 4 primeras páginas a la vez que se almacenan los datos en las listas anteriormente creadas
for i in range(0,3):
    for hotel in page.findAll('div',attrs={'class':'d20f4628d0'}):
                    title=hotel.find("div",attrs={'fcab3ed991 a23c043802'})
                    if title:
                        titulo_.append(title.text)
                    else: titulo_.append('')
                    location=hotel.find("span",attrs={'data-testid':'address'})
                    if location:
                        localizacion_.append(location.text)
                    else: localizacion_.append('')
                    comment=hotel.find("div",attrs={'class':'b5cd09854e f0d4d6a2f5 e46e88563a'})
                    if comment:
                        valoracion_.append(comment.text)
                    else: valoracion_.append('')
                    commentaries=hotel.find("div",attrs={'class':'d8eab2cf7f c90c0a70d3 db63693c62'})
                    if commentaries:
                        comentarios_.append(commentaries.text)
                    else: comentarios_.append('')
                    rate=hotel.find("div",attrs={'class':'b5cd09854e d10a6220b4'})
                    if rate:
                        puntuacion_.append(rate.text)
                    else: puntuacion_.append('')
                    distance=hotel.find("span",attrs={'data-testid':'distance'})
                    if distance:
                        distancia_.append(distance.text)
                    else: distancia_.append('')
                    bed=hotel.find("span",attrs={'class':'df597226dd'})
                    if bed:
                        condiciones_alojamiento_.append(bed.text)
                    else: condiciones_alojamiento_.append('')
                    situation=hotel.find("span",attrs={'class':'f9afbb0024'})
                    if situation:
                        situacion_.append(situation.text)
                    else: situacion_.append('')
                    price=hotel.find("span",attrs={'class':'c5888af24f e729ed5ab6'})
                    if price:
                        precio_anterior_.append(price.text)
                    else: precio_anterior_.append('')
                    precio_actual=hotel.find("span",attrs={'class':'fcab3ed991 fbd1d3018c e729ed5ab6'})
                    if precio_actual:
                        precio_actual_.append(precio_actual.text)
                    else: precio_actual_.append('')
                    
                    
    driver.find_element(By.CSS_SELECTOR,'#search_results_table > div:nth-child(2) > div > div > div > div.d7a0553560 > div.b727170def > nav > div > div.f32a99c8d1.f78c3700d2 > button > span > svg').click()
    time.sleep(5)
    
# Se crea el dataset final
Hotels_dataset=pd.DataFrame({
                                'Titulo':titulo_,
                                'Ubicación':localizacion_,
                                'Valoración':valoracion_,
                                'Número de comentarios':comentarios_,
                                'Puntuación':puntuacion_,
                                'Distancia del cento':distancia_,
                                'Condiciones del alojamiento':condiciones_alojamiento_,
                                'Situación':situacion_,
                                'Precio anterior':precio_anterior_,
                                'Precio actual':precio_actual_
                                
})


# Se almacena el dataset en un archivo csv


Hotels_dataset.to_csv(r"D:/43591894v/Downloads/Hotels_dataset.csv", index=None, header=True, encoding='utf-8-sig')


driver.quit()


# In[ ]:




