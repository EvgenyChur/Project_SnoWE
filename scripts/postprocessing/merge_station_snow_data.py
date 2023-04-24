# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 15:50:35 2018

@author: Evgenii Churiulin
Программа для работы с метеорологическими данными, полученными из SYNOP кода с помощью скрипта (все данные в 1 файле) на tornado 
Программа осуществляет расчет среднесуточных значений метеорологических параметров


"""
import pandas as pd
import os
import datetime
import numpy as np

"""
#Версия для работы по одной станции
fileName = '26825.csv'
iPath = 'D:/Churyulin/msu_cosmo/Data_Natalia_Leonidovna/Data/{}'.format(fileName)
"""


#Путь к папке, где хранится исходная метеорологическая информация

#Первичный счет
#data = 'D:/Churyulin/DON/meteo_2000_2010/'
data = 'D:/Churyulin/DVINA/2011-2019/'

#Для слияния
#data_1 = 'D:/Churyulin/DON/result_2000_2010/' 
#data_2 = 'D:/Churyulin/DON/result_2011_2019/'


#data = 'D:/Churyulin/msu_cosmo/Moscow_data/2000 - 2010/'
#data = 'D:/Churyulin/snow data(ivan)/precipitation/'
#data = 'D:/Churyulin/snow data(ivan)/inna_meteo_real/'
#data = 'D:/Churyulin/Ivan/data/' # путь к данным по запросу студента Вани
#data = 'D:/Churyulin/msu_cosmo/forecast/meteorological_data_oper/' #путь к данным по запросу Инны Николаевны для Северной Двины

#Первичный счет
dirs_csv = sorted(os.listdir(data))

#Для слияния
#dirs_csv_1 = sorted(os.listdir(data_1))
#dirs_csv_2 = sorted(os.listdir(data_2))


#result_exit = 'D:/Churyulin/DON/result_2000_2010/'
result_exit = 'D:/Churyulin/DVINA/result_2011_2019/'
#result_exit = 'D:/Churyulin/DON/final/'


#result_exit = 'D:/Churyulin/msu_cosmo/Data_Natalia_Leonidovna/Result_2000_2010/'
#result_exit = 'D:/Churyulin/msu_cosmo/Moscow_data/result_2000_2010/'
#result_exit = 'D:/Churyulin/snow data(ivan)/result_data/'
#result_exit = 'D:/Churyulin/snow data(ivan)/inna_meteo_1day/'
#result_exit = 'D:/Churyulin/Ivan/result/' # путь к данным (результат) для студента Вани
#result_exit = 'D:/Churyulin/msu_cosmo/forecast/in_situ_oper/' #путь к данным по запросу Инны Николаевны для Северной Двины

dirs_exit = os.listdir(result_exit) #Очистка результатов предыдушей работы скрипта, для получения лучшего результатат
for file in dirs_exit:
    os.remove(result_exit + file)

#Работа с временным рядом по метеостанции
for data_file in dirs_csv:
    fileName_csv = data_file
    #Первичный счет
    iPath_1 = (data + fileName_csv)
    #Для слияния 1 и 2 источника в один
    #iPath_1 = (data_1 + fileName_csv)
    #iPath_2 = (data_2 + fileName_csv)
    
    #df = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, header = None, skipinitialspace = True, na_values= ['9990',9990.0,'******','********'])
    df = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, header = None, skipinitialspace = True, na_values= ['******','********'])
    df = df.drop_duplicates(keep = False)
    df=df.drop([5,6,13,14,15,16,17,18,19,20,21,22,23,24,28,33,34,35,36,37,38,39,40,41,42,43,44,45,46], axis=1)
    df.columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    #print ('Columns:'), df.columns
    date = pd.to_datetime(df[0])
    index_meteo = pd.Series(df[1].values, index = date, dtype = 'float')
    lat = pd.Series(df[2].values, index = date, dtype = 'float')
    lon = pd.Series(df[3].values, index = date, dtype = 'float')
    height = pd.Series(df[4].values, index = date, dtype = 'float')
    ps = pd.Series(df[5].values, index = date, dtype = 'float')
    pmsl = pd.Series(df[6].values, index = date, dtype = 'float')
    t2m = pd.Series(df[7].values, index = date, dtype = 'float')
    td2m = pd.Series(df[8].values, index = date, dtype = 'float')
    dd10m = pd.Series(df[9].values, index = date, dtype = 'float')
    ff10m = pd.Series(df[10].values, index = date, dtype = 'float')
    tmin2m = pd.Series(df[11].values, index = date, dtype = 'float')
    tmax2m = pd.Series(df[12].values, index = date, dtype = 'float')
    tming = pd.Series(df[13].values, index = date, dtype = 'float')
    R12 = pd.Series(df[14].values, index = date, dtype = 'float')
    # R12 = R12.replace(9990, np.nan)
    R12[ R12 == 9990.0 ] =  np.nan
    R24 = pd.Series(df[15].values, index = date, dtype = 'float')
    R24[ R24 == 9990.0 ] =  np.nan
    t_g = pd.Series(df[16].values, index = date, dtype = 'float')
    hsnow = pd.Series(df[17].values, index = date, dtype = 'float')

    
    index_meteo = index_meteo.resample('d').mean()
    lat = lat.resample('d').mean()
    lon = lon.resample('d').mean()
    height = height.resample('d').mean()    
    ps = ps.resample('d').mean()
    pmsl = pmsl.resample('d').mean()
    t2m = t2m.resample('d').mean()
    td2m = td2m.resample('d').mean()
    dd10m = dd10m.resample('d').mean()
    ff10mean = ff10m.resample('d').mean()
    ff10max = ff10m.resample('d').max()
    tmin2m = tmin2m.resample('d').mean()
    tmax2m = tmax2m.resample('d').mean()
    tming = tming.resample('d').mean()
    R12 = R12.resample('d').mean()
    R24 = R24.resample('d').mean()
    t_g = t_g.resample('d').mean()
    hsnow = hsnow.resample('d').mean()
    
    """
    index_meteo = index_meteo.resample('M').mean()
    lat = lat.resample('M').mean()
    lon = lon.resample('M').mean()
    height = height.resample('M').mean()    
    ps = ps.resample('M').mean()
    pmsl = pmsl.resample('M').mean()
    t2m = t2m.resample('M').mean()
    td2m = td2m.resample('M').mean()
    dd10m = dd10m.resample('M').mean()
    ff10mean = ff10m.resample('M').mean()
    ff10max = ff10m.resample('M').max()
    tmin2m = tmin2m.resample('M').mean()
    tmax2m = tmax2m.resample('M').mean()
    tming = tming.resample('M').mean()
    R12 = R12.resample('M').sum()
    R24 = R24.resample('M').sum()
    t_g = t_g.resample('M').mean()
    hsnow = hsnow.resample('M').mean()
    """
    #Cоединяем данные в один датафрейм 
    index_meteo.index = lat.index = lon.index = height.index = ps.index = pmsl.index = t2m.index = td2m.index = dd10m.index = ff10mean.index = ff10max.index = tmin2m.index = tmax2m.index = tming.index = R12.index = R24.index = t_g.index = hsnow.index 
    df_data = pd.concat([index_meteo, lat, lon, height, ps, pmsl, t2m,
                         td2m, dd10m, ff10mean, ff10max, tmin2m, tmax2m, tming,
                         R12,R24, t_g, hsnow], axis = 1)

    df_data.to_csv(result_exit + fileName_csv[0:5] +'.csv', sep=';', float_format='%.3f',
                   header = ['index','lat','lon','height','ps','pmsl','t2m','td2m',
                             'dd10m','ff10meanm', 'ff10max','tMin2m','tMax2m','tMinG','R12','R24',
                             't_g','hSnow'], index_label = 'Date')
    

    
    #Версия скрипта для последующего слияния 1 и 2 части в один общий документ
    """
    df_1 = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                       skipinitialspace = True, na_values= ['******','********'])
       
    df_2 = pd.read_csv(iPath_2, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                       skipinitialspace = True, na_values= ['******','********'])
    
    df_data = pd.concat([df_1, df_2])
    df_data.to_csv(result_exit + fileName_csv[0:5] +'.csv', sep=';', float_format='%.3f',
                   header = ['index','lat','lon','height','ps','pmsl','t2m','td2m',
                             'dd10m','ff10m','tMin2m','tMax2m','tMinG','R12','R24',
                             't_g','hSnow'], index_label = 'Date')
    """
    
