#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 18:30:11 2020
This script shows the results for required tutorial of lab 08, including 
prelimary stats and graphic analysis for arctic oscillation and north atlantic
oscillation time series dataset, some slight adjustment on the original code
has to be made so the figures do not look distorted when running the script in
one go, including module matplotlib

questions in assignment related to this tutorial:
    the two dataset do indeed have different length, since they both have 800 
    plus data points, it's easier to use the shorter length (difference is only
    1) so there's no NaN value to deal with when they merge.
@author: wang2846
"""

# import modules
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
pd.set_option('display.max_rows',15) # this limit maximum numbers of rows
# read file into dataframe (df)
ao = np.loadtxt('monthly.ao.index.b50.current.ascii')
# check df
ao[0:2]
ao.shape
# generate dates as the same shape as dataframe
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')
# check df
dates
dates.shape
# extract values
AO = Series(ao[:,2], index=dates)
# check
AO
# initial plots w/ different ranges
plt.figure()
AO.plot()
plt.title('Daily Atlantic Oscillation')
plt.savefig('Daily_AO.pdf')
#AO['1980':'1990'].plot()
#AO['1980-05':'1981-03'].plot()
# slight modification so the plot doesn't look distorted
plt.figure()
AO_range = DataFrame({'whole': AO, '80-90': AO['1980':'1990'], 
                      '05-03': AO['1980-05':'1981-03']})
AO_range.plot(subplots=True, sharex=False, layout=(3,1), legend=False)
# accesing values
AO[120]
AO['1960-01']
AO['1960']
AO[AO > 0]
## NAO series
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)
# combine dataframe
plt.figure()
aonao = DataFrame({'AO' : AO, 'NAO' : NAO})
aonao.plot(subplots=True, layout=(2,1), legend=False)
# data check
aonao.head()
aonao['NAO']
aonao.NAO
# get difference and display start of df
aonao['Diff'] = aonao['AO'] - aonao['NAO']
aonao.head()
# delete new column and checn end of df
del aonao['Diff']
aonao.drop(aonao.tail(1).index, inplace=True) # dropped last row where NAO is NaN
aonao.tail()
# slicing
aonao['1981-01':'1981-03']
# plot selected data from df with specified filter as bar graph
import datetime
plt.figure()
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0) 
        & (aonao.index > datetime.datetime(1980,1,1)) 
        & (aonao.index < datetime.datetime(1989,1,1)),
        'NAO'].plot(kind='barh')
# simple stats
aonao.mean()
aonao.max()
aonao.min()
aonao.mean(1) # row wise
aonao.describe()
# resampling w/ different method
plt.figure()
AO_mm1 = AO.resample("A").mean() # use mean/default
AO_mm1.plot(style='g--')
plt.figure()
AO_mm2 = AO.resample("A").median() # use median
AO_mm2.plot()
plt.title('Annual Median Values for AO')
plt.savefig('Annual Median Values for AO.pdf')
plt.figure()
AO_mm3 = AO.resample("3A").apply(np.max) # use np.max and change frequency to 3 years
AO_mm3.plot()
# all three method used as a list then plot separately and on the same figure
AO_mm = AO.resample("A").apply(['mean', np.min, np.max])
plt.figure()
AO_mm['1900':'2020'].plot(subplots=True, legend=False)
plt.figure()
AO_mm['1900':'2020'].plot()
AO_mm # check newly calculated df
# moving stats
plt.figure()
aonao.rolling(window=12, center=False).mean().plot(style=['-g','-r']) # changed color
plt.title('Rolling Mean for AO & NAO')
plt.savefig('Rolling Mean for AO & NAO.pdf')
plt.figure()
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g') # rolling correlation
aonao.corr() # get correlation