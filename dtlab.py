# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:19:03 2020

@author: User
"""
import numpy as np
import pandas as pd
import timeit
from numpy import lib

def createdf(): #создача фрейма   #загрузить все в 1 датафрейм #18.35 с       
    df = pd.read_csv("household_power_consumption.txt",sep=';') 
    df.columns = ['Date', 'Time', 'GAP', 'GRP', 'Voltage', 'Intensity', 'sm1', 'sm2', 'sm3']
    df.dropna(how='any', inplace=True)
    df['DateTime'] = pd.to_datetime(df['Date'] + df['Time'],format="%d/%m/%Y%H:%M:%S") #классная тема, пандасы продумали хитрость
    df.drop(columns = ['Date', 'Time'], inplace=True)    #беру свої слова назад, це не дейттайм з дейттайму
    df.set_index('DateTime', inplace=True) #ну да, а теперь, когда оно индекс, все работает и это дейттайм а не дейттайм64. наверное 
    for column in df.columns: #потому-что это структура а не дейттайм64(нс)? пожалуйста, поясните, почему из-за отчаяного сетиндекса оно стало работать
        #if column != "DateTime": пережиток прошлого, когда оно небыло индексом
        df[column] = df[column].astype('float32') #с интом что бы сравнить
    return(df)
    
def fivekV(df): #0.022 - 0.029 c
    return df[(df.GAP >= 5)]
   
    
def voltage(df): #0.21 - 0.22 c
    #vt = vt['Voltage']    
    return df[(df.Voltage >= 235)]


def a1920(df): #0.114 c
    return df[(df.Intensity >= 19) & (df.Intensity <= 20)&(df.sm2 > df.sm3)]


def random_and_mid(df): #0.29.8 - 0.301 c
    rf=df.sample(500000)
    print(rf)
    print("середні:")
    mf=rf[['sm1','sm2','sm3']]
    mf=mf.mean()
    print(mf) # на случай если нужно соеденить 4 и 5
    #return(mf)
    
def after6pm(df): #0.232
    a6 = df[(df.index.hour >= 18)]
    a6 = a6[(a6.GAP > 6) & (a6.sm2 > a6.sm1) & (a6.sm2 > a6.sm3)]
    number = len(a6)
    onehalf = int(number/2)
    a6_1 = a6[:onehalf]
    a6_1 = a6_1[::3]
    a6 = a6[onehalf:]
    a6 = a6[::4]
    a6_1 = a6_1.append(a6)
    return (a6_1)
    
    #t = timeit.Timer(lambda: createdf())
    #print (t.timeit(number=1))
    
def profile(df, function):
    t = timeit.Timer(lambda: function(df))
    return t.timeit(number=10)


'''0.0069339120000222465
0.0061736889999792766
0.006121867000047132
0.007385156000054849
0.01288906800004952
0.059990095999864934'''