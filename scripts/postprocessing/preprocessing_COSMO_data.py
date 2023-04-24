# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 13:57:38 2018

@author: Evgeny Churiulin
Скрипт позволяет работать с данными приходящими из модели Космо и осреднять их
"""
import pandas as pd
import os
import gc

def cosmo(iPath, fileName, outPath):
    #fileName = 'data20160101.txt' # Name of the meteorological station - model version
    #iPath_1 = 'C:/Python_script/msu_cosmo/{}'.format(fileName)
    widths = [6,2,2,2,2, 8, 4, 6, 12, 12, 11, 12, 12, 12] 
    df = pd.read_fwf(iPath, widths=widths, skiprows=8, skip_footer=0, header = 0) 
    #df.columns = ['YYYY', 'MM', 'DD', 'HH','mm','LEVEL','GPI','GPJ','RLON','RLAT',
    #'T_2M','TD_2M','RELHUM_2M','QV_S','TOT_PREC']
    df.columns = ['YYYY', 'MM', 'DD', 'HH','mm','LEVEL','GPI','GPJ','RLON','RLAT',
                  'T_2M','TD_2M','RELHUM_2M','QV_S']
    #print 'Columns:', df.columns 

    year = df.iloc[:,0]
    month = df.iloc[:,1]
    day = df.iloc[:,2]
    hour = df.iloc[:,3]
    #minute = df.iloc[:,4]
    meteo_dates = [pd.to_datetime('{}-{}-{}-{}'.format(i, j, z, k), format='%Y-%m-%d-%H') for i,j,z,k in zip(year, month,day,hour)] 
    gpi = pd.Series(df['GPI'].values, index=meteo_dates)
    gpj = pd.Series(df['GPJ'].values, index=meteo_dates)
    rlon = pd.Series(df['RLON'].values, index=meteo_dates)
    rlat = pd.Series(df['RLAT'].values, index=meteo_dates)
    t_2m = pd.Series(df['T_2M'].values, index=meteo_dates)
    td_2m = pd.Series(df['TD_2M'].values, index=meteo_dates)
    relhum_2m = pd.Series(df['RELHUM_2M'].values, index=meteo_dates)
    qv_s = pd.Series(df['QV_S'].values, index=meteo_dates)
    #tot_prec = pd.Series(df['TOT_PREC'].values, index=meteo_dates) #ожидание

    gpi.index = gpj.index = rlon.index = rlat.index = t_2m.index = td_2m.index = relhum_2m.index = qv_s.index
    df_2 = pd.concat([gpi, gpj, rlon, rlat, t_2m, td_2m, relhum_2m, qv_s], axis = 1)
    df_2.columns = ['GPI','GPJ','RLON','RLAT','T_2M','TD_2M','RELHUM_2M','QV_S']
    df_3 = df_2.groupby(['GPI','GPJ'], as_index=False).mean()
    #print df_3
    
    """
    gpi.index = gpj.index = tot_prec.index
    df_prec = pd.concat([gpi, gpj, tot_prec], axis = 1)
    df_prec.columns = ['GPI','GPJ','TOT_PREC']

    df_prec_itog = df_prec.groupby(['GPI','GPJ']).max()
    df_4 = pd.concat([df_3,df_prec_itog], axis =1)
    """
    
    #df_4.to_excel(outPath + 'data_' + fileName[4:12]+'.xlsx', float_format = '%.3f')
    df_3.to_csv(outPath + 'data_' + fileName[4:12]+'.txt', sep = ',', float_format = '%.3f')
    print ('calculated: ' + fileName[4:12])
    gc.collect()

"""
#Чтение файлов из директории
path_1 = 'C:/Python_script/msu_cosmo/2012/'
path_2 = 'C:/Python_script/msu_cosmo/2013/'
path_3 = 'C:/Python_script/msu_cosmo/2014/'
path_4 = 'C:/Python_script/msu_cosmo/2015/'
path_5 = 'C:/Python_script/msu_cosmo/2016/'
"""

#Чтение файлов из директории - данные для прогноза
path_1 = 'D:/Churyulin/msu_cosmo/forecast/0-24/'
path_2 = 'D:/Churyulin/msu_cosmo/forecast/24-48/'
path_3 = 'D:/Churyulin/msu_cosmo/forecast/48-72/'

"""
#Запись результатов по директориям
out_path_1 = 'C:/Python_script/msu_cosmo/results/2012/'
out_path_2 = 'C:/Python_script/msu_cosmo/results/2013/'
out_path_3 = 'C:/Python_script/msu_cosmo/results/2014/'
out_path_4 = 'C:/Python_script/msu_cosmo/results/2015/'
out_path_5 = 'C:/Python_script/msu_cosmo/results/2016/'
"""
#Запись результатов по директориям - данные для прогноза
out_path_1 = 'D:/Churyulin/msu_cosmo/forecast/result_oper/0-24/'
out_path_2 = 'D:/Churyulin/msu_cosmo/forecast/result_oper/24-48/'
out_path_3 = 'D:/Churyulin/msu_cosmo/forecast/result_oper/48-72/'


"""
dirs_cosmo_2012 = os.listdir(path_1)
dirs_cosmo_2013 = os.listdir(path_2) 
dirs_cosmo_2014 = os.listdir(path_3)
dirs_cosmo_2015 = os.listdir(path_4) 
dirs_cosmo_2016 = os.listdir(path_5)
"""
dirs_cosmo_0_24 = os.listdir(path_1)
dirs_cosmo_24_48 = os.listdir(path_2) 
dirs_cosmo_48_72 = os.listdir(path_3)

"""
#Чтение из директории по данным cosmo за 2012
for file in dirs_cosmo_2012:
    fileName_1 = file
    iPath_1 = (path_1 + fileName_1)
    data_1 = cosmo(iPath_1, fileName_1, out_path_1)
   
#Чтение из директории по данным cosmo за 2013  
for file in dirs_cosmo_2013:
    fileName_2 = file
    iPath_2 = (path_2 + fileName_2)
    data_2 = cosmo(iPath_2, fileName_2, out_path_2)
    
#Чтение из директории по данным cosmo за 2014    
for file in dirs_cosmo_2014:
    fileName_3 = file
    iPath_3 = (path_3 + fileName_3)
    data_3 = cosmo(iPath_3, fileName_3, out_path_3)

#Чтение из директории по данным cosmo за 2015    
for file in dirs_cosmo_2015:
    fileName_4 = file
    iPath_4 = (path_4 + fileName_4)
    data_4 = cosmo(iPath_4, fileName_4, out_path_4)

#Чтение из директории по данным cosmo за 2016    
for file in dirs_cosmo_2016:
    fileName_5 = file
    iPath_5 = (path_5 + fileName_5)
    data_5 = cosmo(iPath_5, fileName_5, out_path_5)
"""

#Чтение из директории по данным cosmo за срок 0 - 24 часа

for file in dirs_cosmo_0_24:
    fileName_1 = file
    iPath_1 = (path_1 + fileName_1)
    data_1 = cosmo(iPath_1, fileName_1, out_path_1)
   

  
#Чтение из директории по данным cosmo за срок 24 - 48 часов 
for file in dirs_cosmo_24_48:
    fileName_2 = file
    iPath_2 = (path_2 + fileName_2)
    data_2 = cosmo(iPath_2, fileName_2, out_path_2)

    
#Чтение из директории по данным cosmo за срок 48 - 72 часа   
for file in dirs_cosmo_48_72:
    fileName_3 = file
    iPath_3 = (path_3 + fileName_3)
    data_3 = cosmo(iPath_3, fileName_3, out_path_3)
    
    # -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:10:16 2018

@author: Evgeny Churiulin
Скрипт предназначен для нахождения осадков для метеорологических станций в данных полученных по Cosmo-Ru ETR
"""
import pandas as pd
import numpy as np
import os
#fileName = 'data_20180101.txt' # Name of the meteorological station - model version
#iPath_1 = 'C:/Python_script/msu_cosmo/forecast/result/test/{}'.format(fileName)

#Функция для считывания данных из файлов
def meteodata_cosmo(iPath):
    #df = pd.read_csv(iPath_csv, sep=';')
    #widths = [3,1,3,1,6,1, 6, 1, 7, 1, 7, 1, 6, 1, 5,1,6,1,10]
    
    #df = pd.read_csv(iPath, widths=widths, skiprows=0, skip_footer=0, header = 0)
    df = pd.read_csv(iPath, sep = ',', header = 0)
    #df.columns = ['GPI','1','GPJ','2','RLON','3','RLAT','4','T_2M','5','TD_2M','6','RELHUM_2M','7','QV_S','8','TOT_PREC','9','ID_station']
    #df = df.drop(['1','2','3','4','5','6','7','8','9'],axis = 1)
    return df

def cosmo_precipitation(iPath, fileName, outPath):
    #Подгружаем информацию из excel файла. В файле excel хранится информация о ближайших узлах 
    fileName_excel = 'Meta.xlsx' # Name of the meteorological station - model version
    iPath_excel = 'D:/Churyulin/msu_cosmo/forecast/{}'.format(fileName_excel)
    data_meta = pd.read_excel(iPath_excel)
    index_id = data_meta.iloc[:,0]
    lon_point = data_meta.iloc[:,5]
    lat_point = data_meta.iloc[:,6]
    lon_point.index = lat_point.index = index_id.index
    df_4 = pd.concat([lon_point, lat_point, index_id], axis = 1)
    df_4.columns = ['GPI','GPJ','ID_station']
    
    #Считываем исходную метеорологическую информацию из данных по модели COSMO-Ru
    widths = [3,1,3,1,6,1, 6, 1, 7, 1, 7, 1, 6, 1, 5,1,7]  
    df = pd.read_fwf(iPath, widths=widths, skiprows=0, skip_footer=0, header = 0) 
    #print 'Columns:', df_test.columns 
    gpi = df.iloc[:,0]
    gpj = df.iloc[:,2]
    rlon = df.iloc[:,4]
    rlat = df.iloc[:,6]
    t_2m = df.iloc[:,8]
    td_2m = df.iloc[:,10]
    relhum_2m = df.iloc[:,12]
    qv_s = df.iloc[:,14]
    tot_prec = df.iloc[:,16]

    gpi.index = gpj.index = rlon.index = rlat.index = t_2m.index = td_2m.index = relhum_2m.index = qv_s.index = tot_prec.index
    df_2 = pd.concat([gpi, gpj, rlon, rlat, t_2m, td_2m, relhum_2m, qv_s, tot_prec], axis = 1)
    df_2.columns = ['GPI','GPJ','RLON','RLAT','T_2M','TD_2M','RELHUM_2M','QV_S','TOT_PREC']
    
    result = pd.merge(df_2, df_4, on=['GPI','GPJ'], suffixes=['_l', '_r'])
    result.to_csv(outPath + 'data_' + fileName[5:13]+'.csv', float_format = '%.3f', index = False)
        
    print ('calculated: ' + fileName[5:13])
    return result
  
def cosmo_model(data_csv,csv_data, path_exit):
    maket_data = ''
    for file_data in data_csv:
        fileName_csv = file_data
        iPath_csv = (csv_data + fileName_csv)
        
        df_temp = meteodata_cosmo(iPath_csv)
        if len(maket_data)>0:
            maket_data = pd.concat([maket_data, df_temp])
        else:
            maket_data = df_temp
        print ('Идет сортировка данных:')
    #Сортировка данных
    for i in maket_data['ID_station']:
        result_data = maket_data[maket_data['ID_station'].isin([i])]
        result_data=result_data.drop(['ID_station'], axis = 1)
        result_data = result_data.replace(np.nan, 0)
        result_data.to_csv(path_exit + 'data_' + str(i) +'.csv', float_format = '%.3f', index = False)#, mode = 'a')    


#Чтение файлов из директории - данные для прогноза (исходные данные)
path_1 = 'D:/Churyulin/msu_cosmo/forecast/achive/result_archive/0-24/'
path_2 = 'D:/Churyulin/msu_cosmo/forecast/achive/result_archive/24-48/'
path_3 = 'D:/Churyulin/msu_cosmo/forecast/achive/result_archive/48-72/'

#Запись результатов по директориям - данные для прогноза (Выборка метеоузлов, в соответствии с заданными метеостанциями)
out_path_1 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/0 - 24/'
out_path_2 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/24 - 48/'
out_path_3 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/48 - 72/'


dirs_cosmo_0_24 = os.listdir(path_1)
dirs_cosmo_24_48 = os.listdir(path_2) 
dirs_cosmo_48_72 = os.listdir(path_3)


#Чтение из директории по данным cosmo за срок 0 - 24 часа
for file in dirs_cosmo_0_24:
    fileName_1 = file
    iPath_1 = (path_1 + fileName_1)
    data_1 = cosmo_precipitation(iPath_1, fileName_1, out_path_1)
      
#Чтение из директории по данным cosmo за срок 24 - 48 часов 
for file in dirs_cosmo_24_48:
    fileName_2 = file
    iPath_2 = (path_2 + fileName_2)
    data_2 = cosmo_precipitation(iPath_2, fileName_2, out_path_2)
    
#Чтение из директории по данным cosmo за срок 48 - 72 часа   
for file in dirs_cosmo_48_72:
    fileName_3 = file
    iPath_3 = (path_3 + fileName_3)
    data_3 = cosmo_precipitation(iPath_3, fileName_3, out_path_3)

#Запись результатов по директориям - данные для прогноза, отсортированные по станционно
path_exit_1 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/final_result_station/0 - 24/'
path_exit_2 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/final_result_station/24 - 48/'
path_exit_3 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/final_result_station/48 - 72/'

#Файлы в директории, после поиска нужных метеостанций
dirs_precipitation_0_24 = os.listdir(out_path_1)
dirs_precipitation_24_48 = os.listdir(out_path_2)
dirs_precipitation_48_72 = os.listdir(out_path_3)

#Очистка папок для вывода финального результата
dirs_result_1 = os.listdir(path_exit_1)
for file in dirs_result_1:
    os.remove(path_exit_1 + file)
    
dirs_result_2 = os.listdir(path_exit_2)
for file in dirs_result_2:
    os.remove(path_exit_2 + file)
    
dirs_result_3 = os.listdir(path_exit_3)
for file in dirs_result_3:
    os.remove(path_exit_3 + file)

#Запуск сортировки данных по конкретным метеостанциям
data_precipitation_1 = cosmo_model(dirs_precipitation_0_24, out_path_1, path_exit_1)
data_precipitation_2 = cosmo_model(dirs_precipitation_24_48, out_path_2, path_exit_2)
data_precipitation_3 = cosmo_model(dirs_precipitation_48_72, out_path_3, path_exit_3)

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:32:55 2018

@author:Evgeny
"""

import pandas as pd
import numpy as np
import os

#fileName_excel = 'Meta.xlsx' # Name of the meteorological station - model version
#iPath_excel = 'C:/Python_script/msu_cosmo/msu_meteo_real/{}'.format(fileName_excel)

#Функция для считывания данных из файлов
def meteodata_cosmo(iPath):
    #df = pd.read_csv(iPath_csv, sep=';')
    widths = [3,1,3,1,6,1, 6, 1, 7, 1, 7, 1, 6, 1, 5,1,7]  
    df = pd.read_fwf(iPath, widths=widths, skiprows=0, skip_footer=0, header = 0)
    return df

def cosmo_model(data_csv,csv_data, path_exit):
    fileName_excel = 'Meta.xlsx' # Name of the meteorological station - model version
    iPath_excel = 'D:/Churyulin/msu_cosmo/forecast/{}'.format(fileName_excel)
    
    
    #Объявление и назначение массива
    maket_data = ''

    for file in data_csv:
        fileName_csv = file
        iPath_csv = (csv_data + fileName_csv)
        df_temp = meteodata_cosmo(iPath_csv)
        if len(maket_data)>0:
            maket_data = pd.concat([maket_data, df_temp])
        else:
            maket_data = df_temp
        print ('Calculated:')
        
    data_meta = pd.read_excel(iPath_excel)

    index_id = data_meta.iloc[:,0]
    lon_point = data_meta.iloc[:,5]
    lat_point = data_meta.iloc[:,6]

    lon_point.index = lat_point.index = index_id.index
    df_4 = pd.concat([lon_point, lat_point, index_id], axis = 1)
    df_4.columns = ['GPI','GPJ','ID_station']
    #print 'Columns:', df_test.columns 
    gpi = maket_data.iloc[:,0]
    gpj = maket_data.iloc[:,2]
    rlon = maket_data.iloc[:,4]
    rlat = maket_data.iloc[:,6]
    t_2m = maket_data.iloc[:,8]
    td_2m = maket_data.iloc[:,10]
    relhum_2m = maket_data.iloc[:,12]
    qv_s = maket_data.iloc[:,14]
    tot_prec = maket_data.iloc[:,16]

    gpi.index = gpj.index = rlon.index = rlat.index = t_2m.index = td_2m.index = relhum_2m.index = qv_s.index = tot_prec.index
    df_2 = pd.concat([gpi, gpj, rlon, rlat, t_2m, td_2m, relhum_2m, qv_s, tot_prec], axis = 1)
    df_2.columns = ['GPI','GPJ','RLON','RLAT','T_2M','TD_2M','RELHUM_2M','QV_S','TOT_PREC']
    
    result = pd.merge(df_2, df_4, on=['GPI','GPJ'], suffixes=['_l', '_r'])

    #Сортировка данных
    for i in result['ID_station']:
        result_data = result[result['ID_station'].isin([i])]
        result_data=result_data.drop(['ID_station'], axis = 1)
        result_data = result_data.replace(np.nan, 0)
        result_data.to_csv(path_exit + 'data_' + str(i) +'.csv', float_format = '%.3f', index = False)#, mode = 'a')
        return result
#Указание путей к данным входные/выходные данные
path_exit_0_24 = 'C:/Python_script/msu_cosmo/forecast/result/test/0 - 24 result/'
csv_data_0_24 = 'C:/Python_script/msu_cosmo/forecast/result/test/0 - 24/'
path_exit_24_48 = 'C:/Python_script/msu_cosmo/forecast/result/test/24 - 48 result/'
csv_data_24_48 = 'C:/Python_script/msu_cosmo/forecast/result/test/24 - 48/'
path_exit_48_72 = 'C:/Python_script/msu_cosmo/forecast/result/test/48 - 72 result/'
csv_data_48_72 = 'C:/Python_script/msu_cosmo/forecast/result/test/48 - 72/'

dirs_csv_0_24 = os.listdir(csv_data_0_24)
dirs_csv_24_48 = os.listdir(csv_data_24_48)
dirs_csv_48_72 = os.listdir(csv_data_48_72)

#Очистка папок с результатами модельного счета перед выполнением новой расчетной процедуры
dirs_result = os.listdir(path_exit_0_24)
for file in dirs_result:
    os.remove(path_exit_0_24 + file)

dirs_result = os.listdir(path_exit_24_48)
for file in dirs_result:
    os.remove(path_exit_24_48 + file)

dirs_result = os.listdir(path_exit_48_72)
for file in dirs_result:
    os.remove(path_exit_48_72 + file)

#Запуск основной расчетной функции модели
data_1 = cosmo_model(dirs_csv_0_24, csv_data_0_24, path_exit_0_24) 
data_2 = cosmo_model(dirs_csv_24_48, csv_data_24_48, path_exit_24_48) 
data_3 = cosmo_model(dirs_csv_48_72, csv_data_48_72, path_exit_48_72)    

