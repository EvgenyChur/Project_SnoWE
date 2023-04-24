# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:05:32 2018

@author: Evgeny Churiulin
Скрипт предназачен для разбивки метеорологических данных по дате и создания рядов данных пригодных
для дальнейшей работы SNOWE technology (скрипт предназначен для создания макета данных)
"""

import pandas as pd
import os
import numpy as np
#Функция для считывания данных из файлов
def meteodata(iPath):
    df = pd.read_csv(iPath_csv, sep=';')
    return df

#Москвоские метеостанции
#ipath = 'C:/Python_script/snow_mgs_meteo/Result_1day/'
#path_exit = 'D:/Churyulin/msu_cosmo/Moscow_data/result_for_SnoWE/'
#csv_data = 'D:/Churyulin/msu_cosmo/Moscow_data/result_2000_2018/'


#Для задачи Инны
#csv_data = 'D:/Churyulin/snow data(ivan)/inna_meteo_1day/'
#path_exit = 'D:/Churyulin/snow data(ivan)/inna_maket_snowe/'

#Для бассейна реки Дон
csv_data = 'D:/Churyulin/DON/meteo_in_situ_data_2000_2019/'
path_exit = 'D:/Churyulin/DON/snowe_maket/'

#csv_data = 'D:/Churyulin/Murmans/data/'
#path_exit = 'D:/Churyulin/Murmans/rezult/'

#Для северной двины
#path_exit = 'C:/Python_script/msu_cosmo/msu_meteo_real/Maket/'
#csv_data = 'C:/Python_script/msu_cosmo/msu_meteo_real/Meteorological data (1day)/'

dirs_csv = os.listdir(csv_data)

dirs_result = os.listdir(path_exit)
for file in dirs_result:
    os.remove(path_exit + file)
    
#Объявление и назначение массива
maket_data = ''

for file in dirs_csv:
    fileName_csv = file
    #iPath_csv = (ipath + fileName_csv)
    iPath_csv = (csv_data + fileName_csv)
    print (iPath_csv)
    
    df_temp = meteodata(iPath_csv)
    
    if len(maket_data)>0:
        maket_data = pd.concat([maket_data, df_temp])
    else:
        maket_data = df_temp
#print 'Columns:',maket_data.columns[2].strip()
print ('Columns:',maket_data.columns)



#Создание массива со значениями -9999        
data_for_maket = np.full((len(maket_data),2),-9999)
df_zero_values = pd.DataFrame(data=data_for_maket) 

#Получение данные из массивов:
# Первые две строи из массива с -9999 Остальные из метеомассива   
    
defSwe =  df_zero_values.iloc[:,0]
defRho =  df_zero_values.iloc[:,1]
date_array = maket_data['Date'].values
#meteo_dates = pd.date_range('01-01-2000','31-12-2017', freq = '1d')

"""
#Для одного из вариантов
id_code = maket_data['index       '].values
lat = maket_data['lat         '].values
lon = maket_data['lon         '].values
height = maket_data['height      '].values
snowDepth = maket_data['hSnow       '].values
averageT = maket_data['t2m         '].values
maxT = maket_data['tMax2m      '].values                  
p24Sum = maket_data['R24         '].values  
"""





"""
date_array = pd.Series(meteo_dates, name='Date')
id_code = pd.Series(maket_data['index'].values,index=meteo_dates, name='id')
lat = pd.Series(maket_data['lat'].values, index=meteo_dates, name='lat')
lon = pd.Series(maket_data['lon'].values, index=meteo_dates, name='lon')
height = pd.Series(maket_data['height'].values, index=meteo_dates, name='height')
snowDepth = pd.Series(maket_data['hSnow'].values, index=meteo_dates, name='snowDepth')
averageT = pd.Series(maket_data['t2m'].values, index=meteo_dates, name='averageT')
maxT = pd.Series(maket_data['tMax2m'].values, index=meteo_dates, name='maxT')               
p24Sum = pd.Series(maket_data['R24'].values, index=meteo_dates, name='p24Sum')
defSwe = pd.Series(defSwe, name='defSwe')
defRho = pd.Series(defRho, name='defRho') 


date_array = pd.Series(meteo_dates, name='Date')
id_code = pd.Series(maket_data['index'].values, name='id')
lat = pd.Series(maket_data['lat'].values, name='lat')
lon = pd.Series(maket_data['lon'].values, name='lon')
height = pd.Series(maket_data['height'].values, name='height')
snowDepth = pd.Series(maket_data['hSnow'].values, name='snowDepth')
averageT = pd.Series(maket_data['t2m'].values, name='averageT')
maxT = pd.Series(maket_data['tMax2m'].values, name='maxT')               
p24Sum = pd.Series(maket_data['R24'].values, name='p24Sum')
defSwe = pd.Series(defSwe, name='defSwe')
defRho = pd.Series(defRho, name='defRho') 
"""


id_code = maket_data['index'].values
lat = maket_data['lat'].values
lon = maket_data['lon'].values
height = maket_data['height'].values
snowDepth = maket_data['hSnow'].values
averageT = maket_data['t2m'].values
maxT = maket_data['tMax2m'].values                  
p24Sum = maket_data['R24'].values                  

#Преобразование данных к типу series                    
date_array = pd.Series(date_array, name='Date')
id_code = pd.Series(id_code, name='id')
lat = pd.Series(lat, name='lat')
lon = pd.Series(lon, name='lon')
height = pd.Series(height, name='height')
snowDepth = pd.Series(snowDepth, name='snowDepth')
averageT = pd.Series(averageT, name='averageT')
maxT = pd.Series(maxT, name='maxT') 
p24Sum = pd.Series(p24Sum, name='p24Sum')
defSwe = pd.Series(defSwe, name='defSwe')
defRho = pd.Series(defRho, name='defRho') 



#Слияние данных
date_array.index = id_code.index = lon.index = lat.index = height.index = snowDepth.index = maxT.index = averageT.index = p24Sum.index = defSwe.index = defRho.index 
maket = pd.concat([date_array, id_code, lon, lat, height, snowDepth, maxT, averageT,p24Sum,defSwe,defRho], axis = 1 )

#Сортировка данных
for i in maket['Date']:
    #print df.where(df['Date']==i).head()
    #print df[df['Date'].isin([i])].head()
    result_data = maket[maket['Date'].isin([i])]
    #print 'Columns:',result_data.columns
    result_data=result_data.drop(['Date'], axis = 1)
    result_data = result_data.replace(np.nan, 0)
    
       
    #result_data.to_csv(path_exit + 'smfeIn_'+ i+'.csv')# index = False)#, mode = 'a')
    if (i[2] == "." ):
        dstr = i[6:10]+"-"+i[3:5]+"-"+i[0:2]
    else:
        dstr = i
    result_data.to_csv(path_exit + 'smfeIn_'+ dstr+'.txt', sep='\t', encoding='utf-8' ,float_format='%9.3f', index = False)#, mode = 'a')
    #result_data.to_csv(path_exit + 'smfeIn_'+ i+'.txt', sep='\t', float_format='%9.3f', index = False)
    
    print (result_data.head())
    #np.savetxt(path_exit + 'smfeIn_t'+ i+'.txt',result_data, fmt=('%10.0f', '%10.4f', '%10.4f', '%10.3f','%10.3f', '%10.3f', '%10.3f', '%10.3f','%10.3f', '%10.3f'))
    #break
    #with open(path + '{}.csv'.format(i), 'w') as fd:
        #fd.write(str(df[df['Date'].isin([i])]))
        
        #fd.write(str(df[i]))    
 

