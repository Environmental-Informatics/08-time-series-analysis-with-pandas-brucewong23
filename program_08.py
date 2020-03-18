#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:24:54 2020
This script read given discharge data into a dataframe, and produce and save
plots of daily average streamflow, daily average w/ top 10 values marked and 
monthly average streamflow during the recorded period
@author: wang2846
"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# read in data, include datetime, timezone (as instructed), and discharge
# datetime parsed within read_table function, datetime and timezone merged
discharge = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt', 
                          header=26, usecols=[2,3,4],
                          names=['Datetime', 'Timezone', 'Discharge'],
                          parse_dates=[['Datetime', 'Timezone']], 
                          infer_datetime_format=True)
# for dialy average plot, determine date range and daily average
# determine start and end date for daily series
# this is done before set_index, not necessary for plot but available if needed
start_date = str(discharge.Datetime_Timezone[0]).split()[0]
end_date = str(discharge.Datetime_Timezone[len(discharge)-1]).split()[0]
dates = pd.date_range(start=start_date, end=end_date, freq='D')
# determine daily average
discharge_timeid = discharge.set_index('Datetime_Timezone')
daily = discharge_timeid.resample('D').mean()
# plot 
plt.figure()
daily.plot()
#plt.xticks(rotation=45)
plt.xlabel('Datetime')
plt.ylabel('Discharge (cfs)')
plt.title('Daily Average Streamflow')
plt.savefig('Daily Average Streamflow.pdf')
# find top 10 and plot
top10 = daily.nlargest(10, columns='Discharge')
plt.figure()
daily.plot()
plt.scatter(top10.index, top10.Discharge, c='r', marker='^', label='Top 10')
plt.legend()
plt.xlabel('Datetime')
plt.ylabel('Discharge (cfs)')
plt.title('Daily Average Streamflow w/ Top 10 Values')
plt.savefig('Daily Average Streamflow & Top 10.pdf')
# monthly average, resample and plot
monthly = discharge_timeid.resample('M').mean()
plt.figure()
monthly.plot()
plt.xlabel('Datetime')
plt.ylabel('Discharge (cfs)')
plt.title('Monthly Average Streamflow')
plt.savefig('Monthly Average Streamflow.pdf')