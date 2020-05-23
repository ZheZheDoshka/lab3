# -*- coding: utf-8 -*-
"""
Created on Sun May 24 00:14:22 2020

@author: User
"""

import numpy as np
from numpy.lib import recfunctions
import pandas as pd
import timeit
import datetime
import nplab
import dtlab
import matplotlib.pyplot as plt

def profile_dt():
    t = timeit.Timer(lambda: dtlab.createdf()) #пусть будет
    return t.timeit(number=5) 


def profile_np():
    t = timeit.Timer(lambda: nplab.createnp())
    return t.timeit(number=5)

functions = {1 : dtlab.fivekV, 2 : dtlab.voltage, 3 : dtlab.a1920, 4 : dtlab.after6pm} #4 : nplab.random_and_mid нет смысла проверять
functions2 = {1 : nplab.fivekV, 2 : nplab.voltage, 3 : nplab.a1920, 4 : nplab.after6pm}   # так как нельзя взять 500000 строчек из 100
                                                        
def profile(df, function):
    t = timeit.Timer(lambda: function(df))
    return t.timeit(number=10)

def ultra_profile(df,hp, functions,functions2):
    i=1
    while i<5:
        for_plot=[1,1,1,1,1]
        for_np_plot=[1,1,1,1,1]
        x_plot=[10,100,1000,10000,100000]
        m=1
        f=functions.get(i)
        n=functions2.get(i)
        while m<6:
            tens=10**m
            for_plot[m-1]=profile(df[:tens], f)
            for_np_plot[m-1]=profile(hp[:tens], n)
            m=m+1
        plt.plot(x_plot, for_plot, 'b', x_plot, for_np_plot, 'r')
        plt.xlabel(str(f))
        plt.ylabel("sec")
        plt.show()
        print(str(f)+" blue - for df, red - for np")
        i=i+1