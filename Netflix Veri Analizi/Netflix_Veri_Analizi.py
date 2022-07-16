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
netflix =pd.read_csv("C:/Users/maksu/OneDrive/Masaüstü/Global AI2/GlobalAIProject/NetflixOriginals.csv",sep=",",encoding="ISO-8859-1")

print(100*"*")

#1) Veri setine göre uzun soluklu filmler hangi dilde oluþturulmuþtur? Görselleþtirme yapýnýz.
#Language deðerlerini gruplandýrýp ortalamalarýný alalým
language={"Language":netflix[["Language","Runtime"]].groupby("Language").mean().index,"Runtime":netflix[["Language","Runtime"]].groupby("Language").mean()["Runtime"].values}
lan_df=pd.DataFrame(language).sort_values(by='Runtime', ascending=False)
#Sonuç
print("Ortalama sürelere bakýldýðýnda, en uzun soluklu filmlerin dillerinde ilk 5:\n\n", lan_df.head())
#Grafik
plt.bar(x="Language", height="Runtime", data= lan_df,width=0.5)
plt.xticks(rotation=90)

print(100*"*")

#2) 2019 Ocak ile 2020 Haziran tarihleri arasýnda 'Documentary' türünde çekilmiþ filmlerin IMDB deðerlerini bulup görselleþtiriniz.
documentary=netflix[netflix.Genre=="Documentary"][["Genre","Premiere","IMDB Score","Title"]]
#2019 ve 2020 yýllarýný seçmek için tarih tipine dönüþtürme iþlemi yapalým
documentary["Premiere"]=pd.to_datetime(documentary.Premiere)
# tarihi içeren bu sütunu index olarak kullanalým
documentary.index=documentary["Premiere"]
documentary.index.name="Date"
# Ayný Sütundan iki tane olmamasý için premiere sütununu silelim index ile devam edelim
documentary.drop("Premiere", axis=1,inplace=True)
documentary= documentary.loc['2019':'2020']

#index olarak tarihi veridim, gerekli filitrelmeleri yaptým 
print("2019 - 2020 Yýllarýnda Documentary türünde yapýlan filmlerin IMBD puanlarý:\n\n",documentary)

#Grafik
## Yýllara göre kaç adet documentary türünde film çekildiðini gösterelim 
data =documentary["Title"].resample("A").count().values
keys = documentary["Title"].resample("A").count().index
explode = [0.08,0.01]
palette_color = sb.color_palette('bright')
plt.pie(data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')
plt.title("2019-2020 Documentary Türündeki Yapýmlarýn YIllara Göre Daðýlýmý")

## Yýllara Göre IMBD puanlarý gösterimi
plt.bar(x=documentary.loc["2019":"2020"].index, height=documentary["IMDB Score"], data=documentary,width=2)
plt.xticks(rotation=90)
print(100*"*")

print(100*"*")
#3) Ýngilizce çekilen filmler içerisinde hangi tür en yüksek IMDB puanýna sahiptir?

Eng= netflix[netflix.Language =="English"][["Genre","IMDB Score","Title"]]
Eng_Top=pd.DataFrame(Eng.groupby("Genre").max().sort_values(by='IMDB Score', ascending=False).head()) 
#türleri array olarak ayýrýyorum
genre=np.array(Eng_Top.index) 
print(f"ingilizce çekilen yapýmlar arasýnda en yüksek IMBD puanýna sahip ilk 5 þu þekildedir\n\n {Eng_Top}\n\nEn yüksek puaný alan tür: {genre[0:1]} ve puaný: {Eng_Top['IMDB Score'].max()}")
#Grafik
##En yüksek ÝMBD puaný olan ingilizce yapýmlarýn türleri
plt.bar(x=Eng_Top.index, height=Eng_Top["IMDB Score"], data=Eng_Top)
plt.xticks(rotation=90)
print(100*"*")

print(100*"*")
#4) 'Hindi' Dilinde çekilmiþ olan filmlerin ortalama 'runtime' suresi nedir?

hindi=pd.DataFrame({"Language":netflix[["Language","Runtime"]].groupby("Language").mean().index,"Runtime":netflix[["Language","Runtime"]].groupby("Language").mean()["Runtime"].values}) 
print("Hind Filmlerinin ortalama süresi: {}".format(hindi[hindi.Language=='Hindi']["Runtime"]))
print(100*"*")
#5) 'Genre' Sütunu kaç kategoriye sahiptir ve bu kategoriler nelerdir? Görselleþtirerek ifade ediniz.
genre=pd.DataFrame({"Genre":netflix[["Genre","Language"]].groupby("Genre").count().index,"Count":netflix[["Genre","Language"]].groupby("Genre").count()["Language"].values})
print("Genre Sütünundaki kategori sayýsý :{0}".format(genre.Genre.count()))
#Grafik 
data=genre.sort_values(by='Count', ascending=False).head(10)["Count"]
keys = genre.sort_values(by='Count', ascending=False).head(10)["Genre"]
explode =[]
for i in range(10): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Netflix'te En Çok Üretilen Yapým Türlerinin ilk 10 Tanesinin Daðýlýmý")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')

print(100*"*")

#6) Veri setinde bulunan filmlerde en çok kullanýlan 3 dili bulunuz.

language={"Language":netflix[["Language","Title"]].groupby("Language").count().index,"Count":netflix[["Language","Title"]].groupby("Language").count()["Title"].values}
lan_df=pd.DataFrame(language).sort_values(by='Count', ascending=False)
print("Netflix'teki yapýmlarda en çok kullanýlan 3 dil \n{0}".format(lan_df.head(3)))

#Grafik
data=lan_df.head(3)["Count"]
keys =lan_df.head(3)["Language"]
explode =[]
for i in range(3): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Netflix'teki Yapýmlarda En Çok kullanýlan 3 Dilin Daðýlýmý")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')
print(100*"*")
#7) IMDB puaný en yüksek olan ilk 10 film hangileridir?
print("IMDB puaný en yüksek olan ilk 10 film:\n{}".format(netflix[["IMDB Score","Title"]].sort_values(by="IMDB Score",ascending=False).head(10))) 
print(100*"*")

#8) IMDB puaný ile 'Runtime' arasýnda nasýl bir korelasyon vardýr? Ýnceleyip görselleþtiriniz.

#Korelasyon ölçümü
cor = netflix[["IMDB Score","Runtime"]]
print("Runtime ve IMDB puanlarý arasýndaki iliþkiye bakýldýðýnda istatistiksel bir ilþki görülmemektedir. Korelasyon tablosu: \n{}".format(cor.corr()))


#grafik
sb.scatterplot(x="IMDB Score",y="Runtime",data=cor)
sb.lineplot(x="IMDB Score", y="Runtime", data=cor,palette="flare")
print(100*"*")
# 9) IMDB Puaný en yüksek olan ilk 10 'Genre' hangileridir? Görselleþtiriniz.
print(" IMDB Puaný en yüksek olan ilk 10 'Genre': \n{0}".format(netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10)))
#grafik
sb.barplot(x=netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10).index,y=netflix[["IMDB Score","Genre"]].groupby("Genre").max().sort_values(by="IMDB Score",ascending=False).head(10)["IMDB Score"])
plt.xticks(rotation=90)

print(100*"*")
#10) 'Runtime' deðeri en yüksek olan ilk 10 film hangileridir? Görselleþtiriniz.
print("Runtime' deðeri en yüksek olan ilk 10 film:\n{0}".format(netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)))
#Grafik
sb.barplot(x=netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)["Title"],y=netflix[["Runtime","Title"]].sort_values(by="Runtime",ascending=False).head(10)["Runtime"])
plt.xticks(rotation=90)
print(100*"*")

#11) Hangi yýlda en fazla film yayýmlanmýþtýr? Görselleþtiriniz.
## Gerekli
date=netflix[["Premiere","Title"]].groupby("Premiere")["Title"].count()
date.index=pd.to_datetime(date.index)
date.index.name="Date"
date=date.resample("A").count().sort_values(ascending=False)
print("en fazla film yayýmlanan yýl: \n{0}".format(date.head(1)))

print(100*"*")

#12) Hangi dilde yayýmlanan filmler en düþük ortalama IMBD puanýna sahiptir? Görselleþtiriniz.
print("En düþük ortalama IMBD puanýna sahip yapýmýn dili ve IMDB puaný: \n{0}".format(netflix[["IMDB Score","Language"]].groupby("Language").mean().sort_values(by="IMDB Score",ascending=True).head(1)))
#Grafik
X=netflix[["IMDB Score","Language"]].groupby("Language").mean().sort_values(by="IMDB Score",ascending=True)
plt.bar(x=X.index, height=X["IMDB Score"], data=X)
plt.xticks(rotation=90)
print(100*"*")


#13) Hangi yýlýn toplam "runtime" süresi en fazladýr?
date=netflix[["Premiere","Runtime"]].groupby("Premiere")["Runtime"].count()
date.index=pd.to_datetime(date.index)
date.index.name="Date"
date=date.resample("A").mean().sort_values(ascending=False)
print(" Yýllara göre 'runtime' ortalamasý en fazla olan yýl ve ortalamasý: \n{0}".format(date.head(1)))
#grafik

data=date.values

keys =date.index
explode =[]
for i in range(8): 
    explode.append(random.uniform(0.01,0.1)) 
    palette_color = sb.color_palette('dark')
plt.title("Yýllara göre 'runtime' ortalamasýnýn Daðýlýmý")
plt.pie(x=data, labels=keys, colors=palette_color,explode=explode, autopct='%.0f%%')

print(100*"*")
#14) Her bir dilin en fazla kullanýldýðý "Genre" nedir?
print("Netflix'teki yapýmlarýn dillere göre en fazla yayýnladýðý türler: \n{0}".format(netflix[["Language","Genre"]].groupby("Language").max()))
print(100*"*")


#15) Veri setinde outlier veri var mýdýr? Açýklayýnýz.

# Runtime verisi için Outlier incelemesi
print("Runtime verisine bakýldýðýnda, ortalamadan, standart sapmanýn çok üstünde sapma gösteren deðerler vardýr. Bu deðerlere bakýldýðýnda 209 dakikalýk bir yapýmla 4 dakikaklýk bir yapým olduðu görülüyor. Ortalamanýn da yaklaþýk 94 dakika olduðu görülebilir. Detaylar için: \n{0}".format(netflix.Runtime.describe()))
## Runtime Grafik
sb.boxenplot(netflix["Runtime"])

# IMDB Score outlier incelemesi
print("IMDB Score incelendiðinde ortalamasý, standart sapmasý yaklaþýk 1 olan bir daðýlým görünüyor. Alt deðeri 3 ve üst deðeri 9'dur ve bunlar aþýrý deðerlerdir.Burada da Aþýrý deðerlerin olduðu görülmektedir  \n{0}".format(netflix["IMDB Score"].describe()))
##IMDB Score Grafik
sb.boxenplot(netflix["IMDB Score"])












