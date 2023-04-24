# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:14:28 2018

@author: Evgenii Churiulin
Программа предназначена для слияния двух типов однородных данных в один

"""
import pandas as pd
import os
import numpy as np
import math
#fileName = '27858.csv'
#iPath_1 = 'D:/Churyulin/DON/result_2000_2010/{}'.format(fileName)
#iPath_2 = 'D:/Churyulin/DON/result_2011_2019/{}'.format(fileName)


data = 'D:/Churyulin/msu_cosmo/real_meteo/Data/' #Добавление папок идет в ручную, в зависимоти от работы скипта RemDB
dirs_csv = sorted(os.listdir(data))


#data_2000_2011 = 'D:/Churyulin/DON/result_2000_2010/'
data_2000_2011 = 'D:/Churyulin/DVINA/result_2000_2010/'
dirs_csv_2000_2011 = sorted(os.listdir(data_2000_2011))

#data_2011_2019 = 'D:/Churyulin/DON/result_2011_2019/'
data_2011_2019 = 'D:/Churyulin/DVINA/result_2011_2019/'

dirs_csv_2011_2019 = sorted(os.listdir(data_2011_2019))

#path_exit = 'D:/Churyulin/DON/meteo_in_situ_data_2000_2019/' #Ряды данных для метеостанций в бассейне р. Дон
path_exit = 'D:/Churyulin/DVINA/result_2000_2019/' #Ряды данных для метеостанций в бассейне р. Северная Двина
 
dirs_path_exit = os.listdir(path_exit) #Очистка результатов предыдушей работы скрипта, для получения лучшего результатат
for file in dirs_path_exit:
    os.remove(path_exit + file)


for data_file in dirs_csv_2011_2019:
    fileName_csv = data_file
    iPath_1 = (data_2000_2011 + fileName_csv)
    iPath_2 = (data_2011_2019 + fileName_csv)
 
    df_2000_2010 = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                               skipinitialspace = True, na_values= ['9990','********'])

    df_2011_2019 = pd.read_csv(iPath_2, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                               skipinitialspace = True, na_values= ['9990','********'])

    #df_2000_2019 = pd.concat([df_2000_2010, df_2011_2019])
    df_2000_2019 = pd.concat([df_2011_2019])
    df_2000_2019_final = df_2000_2019.drop_duplicates()
    print ('Columns:', df_2000_2019_final.columns)
    df_2000_2019_final = df_2000_2019_final.drop(['lat','lon','height','ps','pmsl','dd10m',
                                                  'ff10meanm','ff10max','tMin2m','tMax2m','tMinG','R12','t_g','hSnow'], axis=1)
    
    """
    index_1 = df_2000_2019_final.iloc[:,0]
    lat = df_2000_2019_final.iloc[:,1]
    lon = df_2000_2019_final.iloc[:,2]
    height = df_2000_2019_final.iloc[:,3]
    ps = df_2000_2019_final.iloc[:,4]
    pmsl = df_2000_2019_final.iloc[:,5]
    t2m = df_2000_2019_final.iloc[:,6]
    td2m = df_2000_2019_final.iloc[:,7]
    dd10m = df_2000_2019_final.iloc[:,8]
    ff10m = df_2000_2019_final.iloc[:,9]
    tmin2m = df_2000_2019_final.iloc[:,10]
    tmax2m = df_2000_2019_final.iloc[:,11]
    tming = df_2000_2019_final.iloc[:,12]
    R12 = df_2000_2019_final.iloc[:,13]
    R24 = df_2000_2019_final.iloc[:,14]
    t_g = df_2000_2019_final.iloc[:,15]
    hsnow = df_2000_2019_final.iloc[:,16]
    """
    index_1 = df_2000_2019_final.iloc[:,0]
    t2m = df_2000_2019_final.iloc[:,1]
    td2m = df_2000_2019_final.iloc[:,2]
    R24 = df_2000_2019_final.iloc[:,3]   
    
    """
    #Коррекция данных по сумме осадков за 24 часа
    for i, xi in enumerate(R24):
        if xi > 99:
            R24[i] = 0
        elif (R24[i]-R24[i-1]) > 50:
            R24[i] = (R24[i+1]+R24[i-1])/2

    #Коррекция данных по сумме осадков за 12 часов
    for e, ei in enumerate(R12):
        if ei > 99:
            R12[e] = 0
        elif (R12[e]-R12[e-1]) > 50:
            R12[e] = (R12[e+1]+R12[e-1])/2        
    #Коррекция данных по высоте снега 
    for h, hi in enumerate(hsnow):
        if hi > 200:
            hsnow[h] = np.nan
        
        elif (hsnow[h]-hsnow[h-1])  > 65:
            hsnow[h] = hsnow[h-1]
            
        if np.isnan(hsnow[h]) and not np.isnan(hsnow[h-1]) and not np.isnan(hsnow[h+1]) :
            
            hsnow[h] = hsnow[h-1]
            print ('Change')
    #Коррекция данных по температуре
    for j,ji in enumerate(t2m):
        if ji > 45:
            t2m[j] = t2m[j-1]
            #print ('attent2222ion')
        elif ji < -45:
            t2m[j] = t2m[j-1]
            #print ('atdfdsfdson')
    #Коррекция данных по температуре точке росы        
    for k, ki in enumerate(td2m):
        if (td2m[k]-td2m[k-1]) > 35:
            td2m[k] = t2m[k-1]
        elif (td2m[k]-td2m[k-1]) < -35:
            td2m[k] = td2m[k-1]    
    #Коррекция данных по минимальной температуре воздуха
    for t, ti in enumerate(tmin2m):
        if (tmin2m[t]-tmin2m[t-1]) > 35:
            tmin2m[t] = tmin2m[t-1]
        elif (tmin2m[t]-tmin2m[t-1]) < -35:
            tmin2m[t] = tmin2m[t-1]
    #Коррекция данных по максимальной температуре воздуха
    for l, li in enumerate(tmax2m):
        if (tmax2m[l]-tmax2m[l-1]) > 35:
            tmax2m[l] = tmax2m[l-1]
        elif (tmax2m[l]-tmax2m[l-1]) < -35:
            tmax2m[l] = tmax2m[l-1]     
    #Коррекция данных по tg
    for q, qi in enumerate(t_g):
        if (t_g[q]-t_g[q-1]) > 60:
            t_g[q] = t_g[q-1]
        elif (t_g[q]-t_g[q-1]) < -60:
            t_g[q] = t_g[q-1]               
            
    """
    #Коррекция данных по сумме осадков за 24 часа
    for i, xi in enumerate(R24):
        if xi > 99:
            R24[i] = 0
        elif (R24[i]-R24[i-1]) > 50:
            R24[i] = (R24[i+1]+R24[i-1])/2                
           
        if np.isnan(R24[i])  :
            
            R24[i] = -99
            print ('Change')           
            
    #Коррекция данных по температуре
    for j,ji in enumerate(t2m):
        if ji > 45:
            t2m[j] = t2m[j-1]
            #print ('attent2222ion')
        elif ji < -45:
            t2m[j] = t2m[j-1]
            #print ('atdfdsfdson')
    #Коррекция данных по температуре точке росы        
    for k, ki in enumerate(td2m):
        if (td2m[k]-td2m[k-1]) > 35:
            td2m[k] = t2m[k-1]
        elif (td2m[k]-td2m[k-1]) < -35:
            td2m[k] = td2m[k-1]   
            
    df_2000_2019_final.to_csv(path_exit + fileName_csv[0:5] +'.csv', sep=';', float_format='%.3f', index_label = 'Date')

#header = ['index','lat','lon','height','ps','pmsl','t2m','td2m',
                            # 'dd10m','ff10m','tMin2m','tMax2m','tMinG','R12','R24',
                            # 't_g','hSnow'], index_label = 'Date')
