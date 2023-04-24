# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 18:21:37 2019
@author: Churiulin Evgeny
Скрипт позволяющий разработанный с целью расчета скорости деструктивного метаморфизма снежного покрова
в условиях постоянно изменяющегося шага по времени.
"""

import pandas as pd
import numpy as np


fileName = 'Snow_1.xlsx'
iPath = 'D:/Churyulin/germania/{}'.format(fileName)
result_exit = 'D:/Churyulin/germania/'

df = pd.read_excel(iPath, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                         skipinitialspace = True, na_values= ['9990','********'])

print ('Columns:', df.columns)
df=df.drop(['ttt','info','hy','hj','t_start','t_stop','U1','U2','U3','U4','Ud','Udd','time','time.1','Tch','T','t','Vcr','Vmax','delta'], axis=1)

df_2 = df[np.isfinite(df['hSnow       '])]

df_3 = df
df_3['delta_Snow'] = df_2['hSnow       '].diff().fillna(0).astype(int)

#df_3 = df.assign(delta_Snow=df_2['hSnow       '].diff().fillna(0).astype(int))

df_3 = df.assign(delta_Time=df_2.index.to_series().diff().fillna(0).astype('timedelta64[h]'))
df_3['speed'] = (df_3['delta_Snow']/df_3['delta_Time'])


"""
df_2 = df[np.isfinite(df['hSnow       '])]   
df_table = df_2.diff()
df['delta_A'] = df_2['hSnow       '].diff().fillna(0).astype(int)
df_3 = df_2.assign(delta_Snow=df_2['hSnow       '].diff().fillna(0).astype(int))
df_3['tvalue'] = df_3.index
df_3['delta'] = (df_3['tvalue']-df_3['tvalue'].shift()).fillna(0)
df_3['ans'] = df_3['delta'].apply(lambda x: x  / np.timedelta64(1,'m')).astype('int64') % (24*60)
df_3['ans'] = df_3['ans'] / 60
df_3['speed'] = (df_3['delta_Snow']/df_3['ans'])
"""

df_zero = np.full((len(df_3),8),np.nan)
df_snow = pd.DataFrame(data=df_zero) 
df_snow.columns = [u'Time, hour',u'delta_sd, sm',u'U_def_avg, sm/hour',
                   u'U_def, %/hour',u'T2m avg',u'T2m max',u'T2m min','veter']
       
#Задание переменных для расчетов
isum = -1
time = 0.0   #Переменная для определения продолжительности случая, в часах
summa_delta_snow = 0.0  #Переменная для расчета суммарного изменения высоты снега
delta_snow = 0.0 #Переменная для расчета суммарного изменения высоты снега, взятая по модулю
speed = 0.0 #Переменная для расчета скорости деформации на 1 шаге
speed_avg = 0.0 #Переменная для расчета средней скорости деформации за весь случай
h_snow = 0.0 #Переменная для записи исходной высоты снега
sd = [] #Список, с информацией о высоте снега за период случая
deformation = 0.0 #Переменная для расчета скорости деформации

# Расчет среднесуточной температуры воздуха
temp_avg = 0.0
temp_avg_list = [] #Список для записи температуры воздуха, за исключением 1-го срока
temperatura_list_1step = [] #Список для записи температуры воздуха, за 1 срок
result_temperatura = []   #Список для обхединения списков
# Расчет максимальной температуры воздуха
temp_max = 0.0
temp_max_list = [] #Список для записи температуры воздуха, за исключением 1-го срока
temperatura_max_list_1step = [] #Список для записи температуры воздуха, за 1 срок
result_temperatura_max = [] #Список для обхединения списков
# Расчет минимальной температуры воздуха
temp_min = 0.0
temp_min_list = [] #Список для записи температуры воздуха, за исключением 1-го срока
temperatura_min_list_1step = [] #Список для записи температуры воздуха, за 1 срок
result_temperatura_min = [] #Список для обхединения списков
#Расчет среднесуточной скорости ветра
veter = 0.0
veter_list = [] #Список для записи температуры воздуха, за исключением 1-го срока
veter_list_1step = [] #Список для записи температуры воздуха, за 1 срок
result_veter = [] #Список для обхединения списков


for i in range(len(df_3['delta_Snow'])):
    if  np.isnan(df_3['delta_Snow'][i]):
        #print(i)
        continue
    elif df_3['delta_Snow'][i] < 0 :
        #Расчет продолжительности всего случая
        time = time + df_3['delta_Time'][i]
        #Расчет суммарного изменения высоты снежного покрова в результате метаморфизма
        summa_delta_snow = (summa_delta_snow + df_3['delta_Snow'][i])
        delta_snow = summa_delta_snow * -1 #Перевод из отрицательной дельты в положительную
        #Расчет средней скорости деформации
        speed = (speed + ((-1 * df_3['speed'][i])*(df_3['delta_Time'][i])))    
        #Выборка h_snow_start
        h_snow = df_3['hSnow       '][i] #определение высоты свежевыпавшего снега
        #sd.append(h_snow) #список, с информацией о высоте снега
        #sd_start = sd[0] # первичная высота снега
        
        
        #Заполенения списка с температурами среднесуточными
        temp_avg = df_3['t2m         '][i]
        temp_avg_list.append(temp_avg)
        #Заполенения списка с температурами максимальными
        temp_max = df_3['tMax2m      '][i]
        temp_max_list.append(temp_max)
        #Заполенения списка с температурами минимальными
        temp_min = df_3['tMin2m      '][i]
        temp_min_list.append(temp_min)
        
        veter =  df_3['ff10m       '][i]
        veter_list.append(veter)
 
    elif df_3['delta_Snow'][i] >= 0 and summa_delta_snow < 0:
        isum = isum +1
      
        #Запись в массив. Переменная продолжительность случая
        df_snow['Time, hour'][isum] = time
       
        #Запись в массив. Переменная дельта снега - для случая
        df_snow['delta_sd, sm'][isum] = delta_snow
        
        #Запись в массив. Скорость деформации снега
        #Расчет скорости деформации
        speed_avg = speed / time
        df_snow['U_def_avg, sm/hour'][isum] = speed_avg
        
        #Запись в массив. Деформация снега
        #Расчет деформации
        deformation = ((delta_snow/sd_start)/time) * 100
        df_snow['U_def, %/hour'][isum] = deformation

        #Расчет среднесуточной температуры воздуха с учетом 1-го шага
        temperatura_list_1step.append(temperatura_avg)
        result_temperatura = temperatura_list_1step + temp_avg_list
        temp_avg_1 = np.nanmean(result_temperatura)
        df_snow['T2m avg'][isum] = temp_avg_1
        
        #Расчет максимальной температуры воздуха с учетом 1-го шага
        temperatura_max_list_1step.append(temperatura_max)
        result_temperatura_max = temperatura_max_list_1step + temp_max_list
        temp_max_1 = np.nanmax(result_temperatura_max)
        df_snow['T2m max'][isum] = temp_max_1
        
        #Расчет минимальной температуры воздуха с учетом 1-го шага
        temperatura_min_list_1step.append(temperatura_min)
        result_temperatura_min = temperatura_min_list_1step + temp_min_list
        temp_min_1 = np.nanmin(result_temperatura_min)
        df_snow['T2m min'][isum] = temp_min_1

        #Расчет скорости ветра с учетом 1-го шага
        veter_avg = np.mean(veter_list)
        
        veter_list_1step.append(veter_1_day)
        result_veter = veter_list_1step + veter_list
        veter_avg = np.nanmean(result_veter)
        df_snow['veter'][isum] = veter_avg         
        
        #Обнуление переменных для новой операции агрегирования
        time = 0.0
        summa_delta_snow = 0.0 
        delta_snow = 0.0
        speed = 0.0 
        speed_avg = 0.0
        h_snow = 0.0
        #sd.clear()
        deformation = 0.0
        #Очистка списков и переменной для расчета среднесуточной температуры воздуха
        temp_avg = 0.0
        temp_avg_list.clear()
        temperatura_list_1step.clear()
        result_temperatura.clear()
        #Очистка списков и переменной для расчета максимальной температуры воздуха
        temp_max = 0.0
        temp_max_list.clear()
        temperatura_max_list_1step.clear()
        result_temperatura_max.clear()
        #Очистка списков и переменной для расчета минимальной температуры воздуха
        temp_min = 0.0
        temp_min_list.clear()
        temperatura_min_list_1step.clear()
        result_temperatura_min.clear()
        #Очистка списков и переменной для расчетов среднесуточной скорости ветра
        veter = 0.0        
        veter_list.clear()
        veter_list_1step.clear()
        result_veter.clear()
         

        sd_start = df_3['hSnow       '][i] 
        temperatura_avg = df_3 ['t2m         '][i]
        temperatura_max = df_3['tMax2m      '][i]
        temperatura_min = df_3['tMin2m      '][i]
        veter_1_day = df_3['ff10m       '][i]
    elif df_3['delta_Snow'][i] >= 0 and summa_delta_snow == 0:
       sd_start = df_3['hSnow       '][i]
       temperatura_avg = df_3 ['t2m         '][i]
       temperatura_max = df_3['tMax2m      '][i]
       temperatura_min = df_3['tMin2m      '][i]
       veter_1_day = df_3['ff10m       '][i]
       
#Удаление лишних строк       
df_result = df_snow[np.isfinite(df_snow['delta_sd, sm'])]
#Вывод в csv файл
df_result.to_csv(result_exit + 'final' +'.csv', sep=';', float_format='%.3f')
            #header = ['index','Sum_delta','','height','ps','pmsl','t2m','td2m',
                      #'dd10m','ff10m','tMin2m','tMax2m','tMinG','R12','R24',
                      #'t_g','hSnow'], index_label = 'Date')
