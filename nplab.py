# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:05:20 2020

@author: User
"""

import numpy as np
from numpy.lib import recfunctions #https://numpy.org/devdocs/user/basics.rec.html
import pandas as pd
import timeit
import datetime

def createnp(): #создача фрейма   #загрузить все в 1 массив  #46.46 c
    hp=np.genfromtxt("household_power_consumption.txt", delimiter=';',
                     dtype=[('GAP','float64'), ('GRP','float64'), ('Voltage','float64'), ('Intensity','float64'), ('sm1','int32'),
                            ('sm2','int32'), ('sm3','int32')],
                     skip_header=1, usecols=range(2,9), missing_values='?') #мне врут
    hp_dt=np.genfromtxt("household_power_consumption.txt", dtype='U', delimiter=';', #уникод, оно не хочет так же класно делить все, а
                     skip_header=1, usecols=(0,1), missing_values='?') #на не-U жалуется своим b'
    hp_data=np.empty(hp.size, dtype='datetime64[s]')        #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #D
    i = 0                                                   #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    while i<hp.size:        
        hp_data[i]=mozhettak(hp_dt[i]) #ну канешно, в функции все работает быстро. АААААААААААААААААААААААААААААААААААа
        i=i+1                                  #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#        temp=hp_dt[i,0]                             #костыли на коде
#        temp2=hp_dt[i,1]                #vernite pandas
#        temp=temp[6:]+"-"+temp[3:5]+"-"+temp[:2]        #AAAAAAAAAAAAAAAAAAAAAAAA
#        hp_data[i:,]=(temp +"T"+ temp2) #AAAAAAAAAAAAaAAAAAAAAA
#        i=i+1                              #я не знаю, как еще нормально переделать этот дуратский нумпай, пусть 2млн итераций будет пару часов работать
    hp=recfunctions.append_fields(hp, 'DateTime', hp_data, usemask=False)                 #15
    return(hp)                                         #я тут вже 10 годин, вбийте мене
 
                                               
def mozhettak(a):            #13
    temp=a[0]
    temp2=a[1]
    if temp[1]!='/':
        if temp[4]!='/':
        #vernite pandas
            temp=temp[6:]+"-"+temp[3:5]+"-"+temp[:2]  
        else:
            temp=temp[5:]+"-0"+temp[3:4]+"-"+temp[:2]
    else:
        if temp[3]!='/':
        #vernite pandas
            temp=temp[5:]+"-"+temp[2:4]+"-0"+temp[:1]  
        else:
            temp=temp[4:]+"-0"+temp[2:3]+"-0"+temp[:1]
    return (temp +"T"+ temp2)
   
def fivekV(a):      #0.58-0.75 c                       #ага, а на 4 задачи ушло 15 минут
    return (a[a['GAP']>5])
   
    
def voltage(a): #0.15-0.16 c
    return (a[a['Voltage']>235])
    
    
def a1920(a):
    return (a[(a['Intensity']>=19)&(a['Intensity']<=20)&(a['sm2']>a['sm3'])])
    

def random_and_mid(a): #0.42 - 0.47
 #   rf=np.random.shuffle(a)
#    rf = rf[:500000,:]
 #   rf=np.random.sample(a, k=500000) 
    rfindex = np.random.choice(np.arange(0,len(a)), 500000, replace=False) #массив 5000000 разных индексов
    rf=a[rfindex]
    means=[ rf['sm1'].mean(axis=0), rf['sm2'].mean(axis=0) ,rf['sm3'].mean(axis=0) ]
    return means

    
def after6pm(a): #0.1 - 0.12 c, но без hour
    #через стр не выходит. Странный тип этот ваш дейттайм64 #17    #я понял что нужно построчно проверять, но не понял
   # a=a[rabotay(a)>18] я сдаюся. Ужастные две недели.              как условие вставить
    a6=a[(a['GAP']>6)&(a['sm2']>a['sm3'])&(a['sm2']>a['sm1'])]
    number=len(a6)
    onehalf=int(number/2)
    a6_1=a6[:onehalf]
    a6_1=a6_1[::3]
    a6=a6[onehalf:]
    a6=a6[::2]
    a6_1=np.append(a6_1,a6)
    return a6_1

    
def hour_extract1(k):
    return str(k)[len(str(k))-8:len(str(k))-6]      #зачем он таков? почему не как дататайм?