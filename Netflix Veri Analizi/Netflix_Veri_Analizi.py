# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 19:05:23 2022

@author: Maksut
"""

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt 
from datetime import datetime as dt
import random
from matplotlib import style
import matplotlib as mpl
#dosya okuma
netflix =pd.read_csv("C:/Users/maksu/OneDrive/Masa�st�/Global AI2/GlobalAIProject/NetflixOriginals.csv",sep=",",encoding="ISO-8859-1")

print(100*"*")

#1) Veri setine g�re uzun soluklu filmler hangi dilde olu�turulmu�tur? G�rselle�tirme yap�n�z.
#Language de�erlerini grupland�r�p ortalamalar�n� alal�m
language={"Language":netflix[["Language","Runtime"]].groupby("Language").mean().index,"Runtime":netflix[["Language","Runtime"]].groupby("Language").mean()["Runtime"].values}
lan_df=pd.DataFrame(language).sort_values(by='Runtime', ascending=False)
#Sonu�
print("Ortalama s�relere bak�ld���nda, en uzun soluklu filmlerin dillerinde ilk 5:\n\n", lan_df.head())
#Grafik
plt.bar(x="Language", height="Runtime", data= lan_df,width=0.5)
plt.xticks(rotation=90)

print(100*"*")

#2) 2019 Ocak ile 2020 Haziran tarihleri aras�nda 'Documentary' t�r�nde �ekilmi� filmlerin IMDB de�erlerini bulup g�rselle�tiriniz.
documentary=netflix[netflix.Genre=="Documentary"][["Genre","Premiere","IMDB Score","Title"]]
#2019 ve 2020 y�llar�n� se�mek i�in tarih tipine d�n��t�rme i�lemi yapal�m
documentary["Premiere"]=pd.to_datetime(documentary.Premiere)
# tarihi i�eren bu s�tunu index olarak kullanal�m
documentary.index=documentary["Premiere"]
documentary.index.name="Date"
# Ayn� S�tundan iki tane olmamas� i�in premiere s�tununu silelim index ile devam edelim
documentary.drop("Premiere", axis=1,inplace=True)
documentary= documentary.loc['2019':'2020']

#index olarak tarihi veridim, gerekli filitrelmeleri yapt�m 
print("2019 - 2020 Y�llar�nda Documentary t�r�nde yap�lan filmlerin IMBD puanlar�:\n\n",documentary)

#Grafik
## Y�llara g�re ka� adet documentary t�r�nde film �ekildi�ini g�sterelim 
data =documentary["Title"].resample("A").count().values
keys = documentary["Title"].resample("A").count().index
explode = [0.08,0.01]
palette_color = sb.color_palette('bright')
plt.pie(data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')
plt.title("2019-2020 Documentary T�r�ndeki Yap�mlar�n YIllara G�re Da��l�m�")

## Y�llara G�re IMBD puanlar� g�sterimi
plt.bar(x=documentary.loc["2019":"2020"].index, height=documentary["IMDB Score"], data=documentary,width=2)
plt.xticks(rotation=90)
print(100*"*")

print(100*"*")
#3) �ngilizce �ekilen filmler i�erisinde hangi t�r en y�ksek IMDB puan�na sahiptir?

Eng= netflix[netflix.Language =="English"][["Genre","IMDB Score","Title"]]
Eng_Top=pd.DataFrame(Eng.groupby("Genre").max().sort_values(by='IMDB Score', ascending=False).head()) 
#t�rleri array olarak ay�r�yorum
genre=np.array(Eng_Top.index) 
print(f"ingilizce �ekilen yap�mlar aras�nda en y�ksek IMBD puan�na sahip ilk 5 �u �ekildedir\n\n {Eng_Top}\n\nEn y�ksek puan� alan t�r: {genre[0:1]} ve puan�: {Eng_Top['IMDB Score'].max()}")
#Grafik
##En y�ksek �MBD puan� olan ingilizce yap�mlar�n t�rleri
plt.bar(x=Eng_Top.index, height=Eng_Top["IMDB Score"], data=Eng_Top)
plt.xticks(rotation=90)
print(100*"*")

print(100*"*")
#4) 'Hindi' Dilinde �ekilmi� olan filmlerin ortalama 'runtime' suresi nedir?

hindi=pd.DataFrame({"Language":netflix[["Language","Runtime"]].groupby("Language").mean().index,"Runtime":netflix[["Language","Runtime"]].groupby("Language").mean()["Runtime"].values}) 
print("Hind Filmlerinin ortalama s�resi: {}".format(hindi[hindi.Language=='Hindi']["Runtime"]))
print(100*"*")
#5) 'Genre' S�tunu ka� kategoriye sahiptir ve bu kategoriler nelerdir? G�rselle�tirerek ifade ediniz.
genre=pd.DataFrame({"Genre":netflix[["Genre","Language"]].groupby("Genre").count().index,"Count":netflix[["Genre","Language"]].groupby("Genre").count()["Language"].values})
print("Genre S�t�nundaki kategori say�s� :{0}".format(genre.Genre.count()))
#Grafik 
data=genre.sort_values(by='Count', ascending=False).head(10)["Count"]
keys = genre.sort_values(by='Count', ascending=False).head(10)["Genre"]
explode =[]
for i in range(10): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Netflix'te En �ok �retilen Yap�m T�rlerinin ilk 10 Tanesinin Da��l�m�")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')

print(100*"*")

#6) Veri setinde bulunan filmlerde en �ok kullan�lan 3 dili bulunuz.

language={"Language":netflix[["Language","Title"]].groupby("Language").count().index,"Count":netflix[["Language","Title"]].groupby("Language").count()["Title"].values}
lan_df=pd.DataFrame(language).sort_values(by='Count', ascending=False)
print("Netflix'teki yap�mlarda en �ok kullan�lan 3 dil \n{0}".format(lan_df.head(3)))

#Grafik
data=lan_df.head(3)["Count"]
keys =lan_df.head(3)["Language"]
explode =[]
for i in range(3): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Netflix'teki Yap�mlarda En �ok kullan�lan 3 Dilin Da��l�m�")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')
print(100*"*")
#7) IMDB puan� en y�ksek olan ilk 10 film hangileridir?
print("IMDB puan� en y�ksek olan ilk 10 film:\n{}".format(netflix[["IMDB Score","Title"]].sort_values(by="IMDB Score",ascending=False).head(10))) 
print(100*"*")

#8) IMDB puan� ile 'Runtime' aras�nda nas�l bir korelasyon vard�r? �nceleyip g�rselle�tiriniz.

#Korelasyon �l��m�
cor = netflix[["IMDB Score","Runtime"]]
print("Runtime ve IMDB puanlar� aras�ndaki ili�kiye bak�ld���nda istatistiksel bir il�ki g�r�lmemektedir. Korelasyon tablosu: \n{}".format(cor.corr()))


#grafik
sb.scatterplot(x="IMDB Score",y="Runtime",data=cor)
sb.lineplot(x="IMDB Score", y="Runtime", data=cor,palette="flare")
print(100*"*")
# 9) IMDB Puan� en y�ksek olan ilk 10 'Genre' hangileridir? G�rselle�tiriniz.
print(" IMDB Puan� en y�ksek olan ilk 10 'Genre': \n{0}".format(netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10)))
#grafik
sb.barplot(x=netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10).index,y=netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10)["IMDB Score"])
plt.xticks(rotation=90)

print(100*"*")
#10) 'Runtime' de�eri en y�ksek olan ilk 10 film hangileridir? G�rselle�tiriniz.
print("Runtime' de�eri en y�ksek olan ilk 10 film:\n{0}".format(netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)))
#Grafik
sb.barplot(x=netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)["Title"],y=netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)["Runtime"])
plt.xticks(rotation=90)
print(100*"*")

#11) Hangi y�lda en fazla film yay�mlanm��t�r? G�rselle�tiriniz.
## Gerekli
date=netflix[["Premiere","Title"]].groupby("Premiere")["Title"].count()
date.index=pd.to_datetime(date.index)
date.index.name="Date"
date=date.resample("A").count().sort_values(ascending=False)
print("en fazla film yay�mlanan y�l: \n{0}".format(date.head(1)))

print(100*"*")

#12) Hangi dilde yay�mlanan filmler en d���k ortalama IMBD puan�na sahiptir? G�rselle�tiriniz.
print("En d���k ortalama IMBD puan�na sahip yap�m�n dili ve IMDB puan�: \n{0}".format(netflix[["IMDB Score","Language"]].groupby("Language").mean().sort_values(by="IMDB Score",ascending=True).head(1)))
#Grafik
X=netflix[["IMDB Score","Language"]].groupby("Language").mean().sort_values(by="IMDB Score",ascending=True)
plt.bar(x=X.index, height=X["IMDB Score"], data=X)
plt.xticks(rotation=90)
print(100*"*")


#13) Hangi y�l�n toplam "runtime" s�resi en fazlad�r?
date=netflix[["Premiere","Runtime"]].groupby("Premiere")["Runtime"].count()
date.index=pd.to_datetime(date.index)
date.index.name="Date"
date=date.resample("A").mean().sort_values(ascending=False)
print(" Y�llara g�re 'runtime' ortalamas� en fazla olan y�l ve ortalamas�: \n{0}".format(date.head(1)))
#grafik

data=date.values

keys =date.index
explode =[]
for i in range(8): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Y�llara g�re 'runtime' ortalamas�n�n Da��l�m�")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')

print(100*"*")
#14) Her bir dilin en fazla kullan�ld��� "Genre" nedir?
print("Netflix'teki yap�mlar�n dillere g�re en fazla yay�nlad��� t�rler: \n{0}".format(netflix[["Language","Genre"]].groupby("Language").max()))
print(100*"*")


#15) Veri setinde outlier veri var m�d�r? A��klay�n�z.

# Runtime verisi i�in Outlier incelemesi
print("Runtime verisine bak�ld���nda, ortalamadan, standart sapman�n �ok �st�nde sapma g�steren de�erler vard�r. Bu de�erlere bak�ld���nda 209 dakikal�k bir yap�mla 4 dakikakl�k bir yap�m oldu�u g�r�l�yor. Ortalaman�n da yakla��k 94 dakika oldu�u g�r�lebilir. Detaylar i�in: \n{0}".format(netflix.Runtime.describe()))
## Runtime Grafik
sb.boxenplot(netflix["Runtime"])

# IMDB Score outlier incelemesi
print("IMDB Score incelendi�inde ortalamas�, standart sapmas� yakla��k 1 olan bir da��l�m g�r�n�yor. Alt de�eri 3 ve �st de�eri 9'dur ve bunlar a��r� de�erlerdir.Burada da A��r� de�erlerin oldu�u g�r�lmektedir  \n{0}".format(netflix["IMDB Score"].describe()))
##IMDB Score Grafik
sb.boxenplot(netflix["IMDB Score"])












