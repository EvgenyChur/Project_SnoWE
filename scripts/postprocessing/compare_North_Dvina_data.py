# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 12:43:12 2019

@author: Evgeny Churiulin

Программа предназначена для обработки и сравнения данных с метеостанций 
для проекта с Инной Крыленко по станциям на удельных водосборах реки Северная Двина

"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter
import math
    
        
minorLocator_1 = AutoMinorLocator (n=4)
minorFormatter_1 = FormatStrFormatter('%.1f')

minorLocator_2 = AutoMinorLocator (n=4)
minorFormatter_2 = FormatStrFormatter('%.1f')


years = mdates.YearLocator() #every year
days = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')

"""
Функция для построения графиков с пятью переменными: Функция строит график ввиде линий и точек
prr_1, prr_2, prr_3, prr_4, prr_5 - основные расчетные переменные, далее по ним будет строиться график 
(нужно чтобы был индекс и значение) - индекс в формате даты с суточной дискретностью
n_3 - подпись заголовка для графика
n_4 - подпись оси y
pr_3, pr_4, pr_5 - пределы по шкале y 
pr_6 - параметр вспомогательныъх делений
l_p - положение легенды
time_step_1,time_step_2 - временной диапазон
"""    

#def plot_6(ax, prr_1, prr_2, prr_3, prr_4, prr_5,prr_6, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2): # для отрисовки гибрида
def plot_5(ax, prr_1, prr_2, prr_3, prr_4, prr_5, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2): # для отрисовки основной части
#def plot_5(ax, prr_1, prr_2, prr_3, prr_4, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):    
    ax.plot(prr_1.index, prr_1, label = '1', color = 'tab:blue', linestyle = '-') #Для SnoWE
    ax.plot(prr_2.index, prr_2, label = '2', color = 'tab:orange', linestyle = '--') #Для Ecomag расчет по космо
    ax.plot(prr_3.index, prr_3, label = '3', color = 'tab:green', linestyle = '-.') #Для Ecomag расчет по станциям
    ax.scatter(prr_4.index, prr_4, label = '4', color = 'tab:red', marker = '^') #Для полевых снегомерных маршрутов
    ax.scatter(prr_5.index, prr_5, label = '5', color = 'tab:purple', marker = 'o') #Для лесных снегомерных маршрутов
    #ax.plot(prr_6.index, prr_6, label = '4', color = 'tab:brown', linestyle = '--') #Данные по модели ECOMAG на основе гибрида COSMO
    ax.set_title(na_3, color = 'black', fontsize = 14)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 14)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)


def plot_7(ax, prr_1, prr_2, prr_3, prr_4, prr_5,prr_6, prr_7, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2): # для отрисовки поправочных коэффициентов    
    ax.plot(prr_1.index, prr_1, label = '1', color = 'tab:blue', linestyle = '-') #Для SnoWE
    ax.plot(prr_2.index, prr_2, label = '2', color = 'tab:orange', linestyle = '--') #Для Ecomag расчет по космо
    ax.plot(prr_3.index, prr_3, label = '3', color = 'maroon', linestyle = '-.') #Для Ecomag расчет по космо с поправочным коэффициентом
    ax.plot(prr_4.index, prr_4, label = '4', color = 'tab:green', linestyle = ':') #Для Ecomag расчет по станциям
    ax.plot(prr_5.index, prr_5, label = '5', color = 'tab:pink', linestyle = '--') #Для Ecomag расчет по станциям с поправочным коэффициентом
    ax.scatter(prr_6.index, prr_6, label = '6', color = 'tab:red', marker = '^') #Для полевых снегомерных маршрутов
    ax.scatter(prr_7.index, prr_7, label = '7', color = 'tab:purple', marker = 'o') #Для лесных снегомерных маршрутов
    
    ax.set_title(na_3, color = 'black', fontsize = 14)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 14)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

"""
Функция для построения графиков с четырмя переменными: Функция строит график ввиде линий и точек
prr_1, prr_2, prr_3, prr_4, prr_5 - основные расчетные переменные, далее по ним будет строиться график 
(нужно чтобы был индекс и значение) - индекс в формате даты с суточной дискретностью
n_3 - подпись заголовка для графика
n_4 - подпись оси y
pr_3, pr_4, pr_5 - пределы по шкале y 
pr_6 - параметр вспомогательныъх делений
l_p - положение легенды
time_step_1,time_step_2 - временной диапазон
""" 
        
def plot_4(ax, prr_1, prr_2, prr_3, prr_4, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):
#def plot_4(ax, prr_1, prr_2, prr_3, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):    
    ax.plot(prr_1.index, prr_1, label = '1', color = 'tab:blue', linestyle = '-') #Для SnoWE
    ax.plot(prr_2.index, prr_2, label = '2', color = 'tab:orange', linestyle = '--') #Фактическая синоптическая информация
    ax.scatter(prr_3.index, prr_3, label = '3', color = 'tab:red', marker = '^') #Для полевых снегомерных маршрутов
    ax.scatter(prr_4.index, prr_4, label = '4', color = 'tab:purple', marker = 'o') #Для лесных снегомерных маршрутов

    ax.set_title(na_3, color = 'black', fontsize = 14)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 14)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

"""
Подготовительная стадия. Цель подготовить исходные данные для работы
"""

"""
#Подгружаем данные о запасе воды в снеге по версии ECOMAG счет по космо
fileName_ecomag = 'snow_ecomag_new.csv'
iPath_ecomag = 'D:/Churyulin/snow data(ivan)/inna_data/{}'.format(fileName_ecomag)
#Путь к папке, где хранятся результаты расчетов по версии ecomag
path_exit_ecomag = 'D:/Churyulin/snow data(ivan)/inna_data_ecomag/'
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_ecomag = os.listdir(path_exit_ecomag) 
for file_ecomag in dirs_path_exit_ecomag:
    os.remove(path_exit_ecomag + file_ecomag)


#Подгружаем данные о запасе воды в снеге по версии ECOMAG счет по станциям
fileName_station = 'snow_meteostation_new.csv'
iPath_station = 'D:/Churyulin/snow data(ivan)/inna_data/{}'.format(fileName_station)
#Путь к папке, где хранятся результаты расчетов по версии ecomag
path_exit_meteostation = 'D:/Churyulin/snow data(ivan)/inna_data_meteostation/'
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_meteostation = os.listdir(path_exit_meteostation) 
for file_meteostation in dirs_path_exit_meteostation:
    os.remove(path_exit_meteostation + file_meteostation)


#Подгружаем данные о запасе воды в снеге по версии ECOMAG счет по КОСМО с региональной СУД
fileName_hybrid = 'snow_hybrid_new.csv'
iPath_hybrid = 'D:/Churyulin/snow data(ivan)/inna_data/{}'.format(fileName_hybrid)
#Путь к папке, где хранятся результаты расчетов по версии ecomag
path_exit_hybrid = 'D:/Churyulin/snow data(ivan)/inna_data_hybrid/'
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_hybrid = os.listdir(path_exit_hybrid) 
for file_hybrid in dirs_path_exit_hybrid:
    os.remove(path_exit_hybrid + file_hybrid)


#Подгружаем данные о запасе воды в снеге по версии ECOMAG счет по КОСМО с поправочными коэффициентами
fileName_cosmo_koef = 'snow_cosmo_koef.csv'
iPath_cosmo_koef = 'D:/Churyulin/snow data(ivan)/inna_data/{}'.format(fileName_cosmo_koef)
#Путь к папке, где хранятся результаты расчетов по версии ecomag
path_exit_cosmo_koef = 'D:/Churyulin/snow data(ivan)/inna_data_cosmo_koef/'
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_cosmo_koef = os.listdir(path_exit_cosmo_koef) 
for file_cosmo_koef in dirs_path_exit_cosmo_koef:
    os.remove(path_exit_cosmo_koef + file_cosmo_koef)



#Подгружаем данные о запасе воды в снеге по версии ECOMAG счет по метеостанциям с поправочным коэффиентом
fileName_meteo_koef = 'snow_meteo_koef.csv'
iPath_meteo_koef = 'D:/Churyulin/snow data(ivan)/inna_data/{}'.format(fileName_meteo_koef)
#Путь к папке, где хранятся результаты расчетов по версии ecomag
path_exit_meteo_koef = 'D:/Churyulin/snow data(ivan)/inna_data_meteo_koef/'
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_meteo_koef = os.listdir(path_exit_meteo_koef) 
for file_meteo_koef in dirs_path_exit_meteo_koef:
    os.remove(path_exit_meteo_koef + file_meteo_koef)






#Подгружаем путь к файлу с маршрутными снегомерными наблюдениями в поле - станции

fileName_field = 'field.csv'
iPath_field = 'D:/Churyulin/snow data(ivan)/result_filter/{}'.format(fileName_field) #основной путь работы
#iPath_field = 'D:/Churyulin/Ivan/survey/result_filter/{}'.format(fileName_field) # путь для вани
#Путь к папке, где хранятся результаты маршрутных снегомерных наблюдений в поле
path_exit_field = 'D:/Churyulin/snow data(ivan)/inna_meteo_field/' #основной путь работы
#path_exit_field = 'D:/Churyulin/Ivan/survey/field/' # путь для вани
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_field = os.listdir(path_exit_field) 
for file_field in dirs_path_exit_field:
    os.remove(path_exit_field + file_field)


#Подгружаем путь к файлу с маршрутными снегомерными наблюдениями в лесу
fileName_forest = 'forest.csv'
iPath_forest = 'D:/Churyulin/snow data(ivan)/result_filter/{}'.format(fileName_forest) #основной путь работы
#iPath_forest = 'D:/Churyulin/Ivan/survey/result_filter/{}'.format(fileName_forest) # путь для вани
#Путь к папке, где хранятся результаты маршрутных снегомерных наблюдений в лесу
path_exit_forest = 'D:/Churyulin/snow data(ivan)/inna_meteo_forest/' #основной путь работы
#path_exit_forest = 'D:/Churyulin/Ivan/survey/forest/' # путь для вани
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_forest = os.listdir(path_exit_forest) 
for file_forest in dirs_path_exit_forest:
    os.remove(path_exit_forest + file_forest)

#Загрузка информации о маршрутных снегомерных наблюдениях в поле
df_route_field = pd.read_csv(iPath_field, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                             skipinitialspace = True, na_values= ['9990','********'])


#Преобразование и выгрузка информации для маршрутов в поле
id_code_field = pd.Series(df_route_field['id_st'].values)
id_code_field = id_code_field.drop_duplicates()
field = []
for i in id_code_field:
    station_field = i 
    field.append(station_field)

for id_station_field in field:
    df_st = df_route_field.loc[df_route_field['id_st'] == id_station_field]
    df_st.to_csv(path_exit_field + str(id_station_field) +'.csv', sep=';', float_format='%.3f')   


#Загрузка информации о маршрутных снегомерных наблюдениях в лесу
df_route_forest = pd.read_csv(iPath_forest, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                              skipinitialspace = True, na_values= ['9990','********'])

#Преобразование и выгрузка информации для маршрутов в лесу
id_code_forest = pd.Series(df_route_forest['id_st'].values)
id_code_forest = id_code_forest.drop_duplicates()
forest = []
for j in id_code_forest:
    station_forest = j 
    forest.append(station_forest)

for id_station_forest in forest:
    df_st_forest = df_route_forest.loc[df_route_forest['id_st'] == id_station_forest]
    df_st_forest.to_csv(path_exit_forest + str(id_station_forest) +'.csv', sep=';', float_format='%.3f') 


#Загрузка информации о запасе воды в снеге по данным ecomag
df_ecomag = pd.read_csv(iPath_ecomag, skiprows = 2, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                        skipinitialspace = True, na_values= ['9990','********'])


df_ecomag = df_ecomag.rename(columns={'601':'22563','604':'23608','612':'23701','670':'23709','672':'22671','706':'22676','708':'22557','709':'23704',
                                      '713':'22559','735':'23803','737':'23707','773':'22781','788':'22651','806':'22656','825':'22798','827':'23804',
                                      '851':'23808','884':'22762','917':'22778','929':'22657','934':'23807','966':'22876','979':'22768','990':'23904',
                                      '997':'22889','1021':'22887','1029':'22888','1047':'22996','1093':'22983','1103':'22869','1105':'22981','1164':'27083',
                                      '1172':'22988','1179':'22867','1227':'22974','1235':'22966','1244':'27071','1325':'27066','1341':'27051','1399':'27044',
                                      '1459':'27026','1536':'27037'})


#list_catchment = [601,604,612,670,672,706,708,709,713,735,737,773,788,806,825,
#                  827,851,884,917,929,934,966,979,990,997,1021,1029,1047,1093,
#                  1103,1105,1164,1172,1179,1227,1235,1244,1325,1341,1399,1459,1536]
list_station = [22563,23608,23701,23709,22671,22676,22557,23704,22559,23803,23707,22781,22651,22656,
                22798,23804,23808,22762,22778,22657,23807,22876,22768,23904,22889,22887,22888,22996,
                22983,22869,22981,27083,22988,22867,22974,22966,27071,27066,27051,27044,27026,27037]

for id_station_ecomag in list_station:
    df_st_ecomag = df_ecomag[str(id_station_ecomag)]
    df_st_ecomag.to_csv(path_exit_ecomag + str(id_station_ecomag) +'.csv', sep=';', float_format='%.3f', header = ['swe'])  


#Загрузка информации о запасе воды в снеге по данным ecomag, но счет по станциям
df_ecomag_station = pd.read_csv(iPath_station, skiprows = 2, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                        skipinitialspace = True, na_values= ['9990','********'])

df_ecomag_station = df_ecomag_station.rename(columns={'601':'22563','604':'23608','612':'23701','670':'23709','672':'22671','706':'22676','708':'22557','709':'23704',
                                                      '713':'22559','735':'23803','737':'23707','773':'22781','788':'22651','806':'22656','825':'22798','827':'23804',
                                                      '851':'23808','884':'22762','917':'22778','929':'22657','934':'23807','966':'22876','979':'22768','990':'23904',
                                                      '997':'22889','1021':'22887','1029':'22888','1047':'22996','1093':'22983','1103':'22869','1105':'22981','1164':'27083',
                                                      '1172':'22988','1179':'22867','1227':'22974','1235':'22966','1244':'27071','1325':'27066','1341':'27051','1399':'27044',
                                                      '1459':'27026','1536':'27037'})


for id_station_ecomag_staion in list_station:
    df_st_ecomag_station = df_ecomag_station[str(id_station_ecomag_staion)]
    df_st_ecomag_station.to_csv(path_exit_meteostation + str(id_station_ecomag_staion) +'.csv', sep=';', float_format='%.3f', header = ['swe'])  

    
#Загрузка информации о запасе воды в снеге по данным ecomag, но счет осуществеляется на основе гибрида
df_ecomag_hybrid = pd.read_csv(iPath_hybrid, skiprows = 2, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                               skipinitialspace = True, na_values= ['9990','********'])

df_ecomag_hybrid = df_ecomag_hybrid.rename(columns={'601':'22563','604':'23608','612':'23701','670':'23709','672':'22671','706':'22676','708':'22557','709':'23704',
                                                    '713':'22559','735':'23803','737':'23707','773':'22781','788':'22651','806':'22656','825':'22798','827':'23804',
                                                    '851':'23808','884':'22762','917':'22778','929':'22657','934':'23807','966':'22876','979':'22768','990':'23904',
                                                    '997':'22889','1021':'22887','1029':'22888','1047':'22996','1093':'22983','1103':'22869','1105':'22981','1164':'27083',
                                                    '1172':'22988','1179':'22867','1227':'22974','1235':'22966','1244':'27071','1325':'27066','1341':'27051','1399':'27044',
                                                    '1459':'27026','1536':'27037'})


for id_station_ecomag_hybrid in list_station:
    df_st_ecomag_hybrid = df_ecomag_hybrid[str(id_station_ecomag_hybrid)]
    df_st_ecomag_hybrid.to_csv(path_exit_hybrid + str(id_station_ecomag_hybrid) +'.csv', sep=';', float_format='%.3f', header = ['swe'])
    
    
#Загрузка информации о запасе воды в снеге по данным ecomag, но счет осуществеляется на основе COSMO данных с поправочным коэффициентом
df_ecomag_cosmo_koef = pd.read_csv(iPath_cosmo_koef, skiprows = 2, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                   skipinitialspace = True, na_values= ['9990','********'])

df_ecomag_cosmo_koef = df_ecomag_cosmo_koef.rename(columns={'601':'22563','604':'23608','612':'23701','670':'23709','672':'22671','706':'22676','708':'22557','709':'23704',
                                                    '713':'22559','735':'23803','737':'23707','773':'22781','788':'22651','806':'22656','825':'22798','827':'23804',
                                                    '851':'23808','884':'22762','917':'22778','929':'22657','934':'23807','966':'22876','979':'22768','990':'23904',
                                                    '997':'22889','1021':'22887','1029':'22888','1047':'22996','1093':'22983','1103':'22869','1105':'22981','1164':'27083',
                                                    '1172':'22988','1179':'22867','1227':'22974','1235':'22966','1244':'27071','1325':'27066','1341':'27051','1399':'27044',
                                                    '1459':'27026','1536':'27037'})


for id_station_ecomag_cosmo_koef in list_station:
    df_st_ecomag_cosmo_koef = df_ecomag_cosmo_koef[str(id_station_ecomag_cosmo_koef)]
    df_st_ecomag_cosmo_koef.to_csv(path_exit_cosmo_koef + str(id_station_ecomag_cosmo_koef) +'.csv', sep=';', float_format='%.3f', header = ['swe'])

#Загрузка информации о запасе воды в снеге по данным ecomag, но счет осуществеляется на основе метео данных с поправочным коэффициентом
df_ecomag_meteo_koef = pd.read_csv(iPath_meteo_koef, skiprows = 2, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                                   skipinitialspace = True, na_values= ['9990','********'])

df_ecomag_meteo_koef = df_ecomag_meteo_koef.rename(columns={'601':'22563','604':'23608','612':'23701','670':'23709','672':'22671','706':'22676','708':'22557','709':'23704',
                                                    '713':'22559','735':'23803','737':'23707','773':'22781','788':'22651','806':'22656','825':'22798','827':'23804',
                                                    '851':'23808','884':'22762','917':'22778','929':'22657','934':'23807','966':'22876','979':'22768','990':'23904',
                                                    '997':'22889','1021':'22887','1029':'22888','1047':'22996','1093':'22983','1103':'22869','1105':'22981','1164':'27083',
                                                    '1172':'22988','1179':'22867','1227':'22974','1235':'22966','1244':'27071','1325':'27066','1341':'27051','1399':'27044',
                                                    '1459':'27026','1536':'27037'})


for id_station_ecomag_meteo_koef in list_station:
    df_st_ecomag_meteo_koef = df_ecomag_meteo_koef[str(id_station_ecomag_meteo_koef)]
    df_st_ecomag_meteo_koef.to_csv(path_exit_meteo_koef + str(id_station_ecomag_meteo_koef) +'.csv', sep=';', float_format='%.3f', header = ['swe'])    







"""

"""
Основная часть работы. Работа с данными и отрисовка материалов.
"""


result_data = 'D:/Churyulin/snow data(ivan)/result_data/'
result_data_stat = 'D:/Churyulin/snow data(ivan)/statistica/'


iPath_plot = 'D:/Churyulin/snow data(ivan)/inna_comparison_plot/'
#Очистка результатов предыдушей работы скрипта
dirs_path_plot = os.listdir(iPath_plot) 
for file_plot in dirs_path_plot:
    os.remove(iPath_plot + file_plot)

list_station_comparison = [22563,22656,22671,22762,22778,22798,22867,22974,22768,22981,22876,23803,
                           22996,23701,23709,23804,23807,23904,27051,27066,27083]
    
#list_station_comparison = [22563,22671,22762,22768,22778,22798,22867,22974,22996,23701,23709,23803,23804,
#                           23807,27051,27066,27083,22876,23904]
#list_station_comparison = [22563,22762,22768,22798,22867,22974,22996,27051,27083,22876] #SNOWE ЛУЧШЕ

#list_station_comparison = [22671,22778,23701,23709,23803,23804,23807,27066,23904] #ECOMAG лучше
#
#list_station_comparison = [22557,22559,22563,22651,22656,22657,22671,22676,22762,22768,22778,22781,22798,22867,
#                           22869,22876,22887,22888,22889,22966,22974,22981,22983,22988,22996,23608,23701,23704,
#                           23707,23709,23803,23804,23807,23808,23904,27026,27037,27044,27051,27066,27071,27083]


for id_station in sorted(list_station_comparison):
    
    #Считывание данных из SnoWE
    fileName_1 = str(id_station) + '.csv'
    fileName_snowe = '000' + str(id_station) + '.txt'
    
    #D:\Churyulin\snow data(ivan)\inna_snowe_result00022563.txt
    iPath_snowe = 'D:/Churyulin/snow data(ivan)/inna_snowe_result/{}'.format(fileName_snowe)
    df_snowe = pd.read_csv(iPath_snowe, skiprows = 0, sep=' ', dayfirst = True, parse_dates = True, index_col = [0],
                           skipinitialspace = True, na_values= ['9990','********'])


    
    iPath_test = 'D:/Churyulin/snow data(ivan)/inna_meteo_1day/{}'.format(fileName_1)
    df_in_situ = pd.read_csv(iPath_test, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                             skipinitialspace = True, na_values= ['9990','********'])


    #Считывание данных из по экомагу (расчет экомага - по данным космо)
    #fileName_1 = '22656.csv'
    iPath_1 = 'D:/Churyulin/snow data(ivan)/inna_data_ecomag/{}'.format(fileName_1)
    df_ecomag_cosmo = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                  skipinitialspace = True, na_values= ['9990','********'])

    #Считывание данных по экомагу (расчет экомага по данным метеостанций)
    iPath_2 = 'D:/Churyulin/snow data(ivan)/inna_data_meteostation/{}'.format(fileName_1)
    df_ecomag_meteostation = pd.read_csv(iPath_2, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                         skipinitialspace = True, na_values= ['9990','********'])

    #Считывание данных по метеостанции (полевой маршрут)
    iPath_3 = 'D:/Churyulin/snow data(ivan)/inna_meteo_field/{}'.format(fileName_1)
    df_field_survey = pd.read_csv(iPath_3, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                  skipinitialspace = True, na_values= ['9990','********'])


    iPath_44 = 'D:/Churyulin/snow data(ivan)/inna_meteo_1day/{}'.format(fileName_1)
    df_meteostation = pd.read_csv(iPath_44, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                  skipinitialspace = True, na_values= ['9990','********'])

    #Считывание данных по метеостанции (лесной маршрут)
    iPath_4 = 'D:/Churyulin/snow data(ivan)/inna_meteo_forest/{}'.format(fileName_1)
    df_forest_survey = pd.read_csv(iPath_4, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                   skipinitialspace = True, na_values= ['9990','********'])

    #Считывание данных по ecomag (версия для гибрида)
    iPath_5 = 'D:/Churyulin/snow data(ivan)/inna_data_hybrid/{}'.format(fileName_1)
    df_ecomag_hybrid = pd.read_csv(iPath_5, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                   skipinitialspace = True, na_values= ['9990','********'])


    #Считывание данных по ecomag (версия для метеорологических станций с поправочным коэффициентом)
    iPath_6 = 'D:/Churyulin/snow data(ivan)/inna_data_meteo_koef/{}'.format(fileName_1)
    df_ecomag_meteo_koef = pd.read_csv(iPath_6, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                       skipinitialspace = True, na_values= ['9990','********'])
    
    #Считывание данных по ecomag (версия для модели космо с поправочным коэффициентом)
    iPath_7 = 'D:/Churyulin/snow data(ivan)/inna_data_cosmo_koef/{}'.format(fileName_1)
    df_ecomag_cosmo_koef = pd.read_csv(iPath_7, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                       skipinitialspace = True, na_values= ['9990','********'])
    
    #periods = 7
    #periods_winter = [['2011-09-01','2012-06-30'],
    #                  ['2012-09-01','2013-06-30'],
    #                  ['2013-09-01','2014-06-30'],
    #                  ['2014-09-01','2015-06-30'],
    #                  ['2015-09-01','2016-06-30'],
    #                  ['2016-09-01','2017-06-30'],
    #                  ['2017-09-01','2018-06-30']]
                  
    #periods = 5
    #periods_winter = [['2013-09-01','2014-06-30'],
    #                  ['2014-09-01','2015-06-30'],
    #                  ['2015-09-01','2016-06-30'],
    #                  ['2016-09-01','2017-06-30'],
    #                  ['2017-09-01','2018-06-30']]

    periods = 1
    periods_winter = [['2013-09-01','2018-05-31']]
                  
        
    periods_winter = np.array(periods_winter)
    #print (periods_winter)
    for tr in range(periods):
        y_w_1 = periods_winter[tr][0]
        y_w_2 = periods_winter[tr][1]
        # Данные о запасе воды в снежном покрове, мм
        snowe_swe = df_snowe['swe'][y_w_1:y_w_2] #Данные по модели SnoWE
        ecomag_model = df_ecomag_cosmo['swe'][y_w_1:y_w_2] #Расчет по экомагу на основе Cosmo-Ru
        ecomag_meteostation = df_ecomag_meteostation['swe'][y_w_1:y_w_2] #Расчет по экомагу на основе данных метеостанцй
        field_in_situ = df_field_survey['swe'][y_w_1:y_w_2] #полевые снегомерные маршруты
        forest_in_situ = df_forest_survey['swe'][y_w_1:y_w_2] #лесные снегомерные маршруты
        ecomag_hybrid = df_ecomag_hybrid['swe'][y_w_1:y_w_2] #Расчет по экомагу на основе COSMO-Ru гибрид
        ecomag_cosmo_koef = df_ecomag_cosmo_koef['swe'][y_w_1:y_w_2] #Расчет по экомагу на основе COSMO-Ru с поправочным коэффициентом
        ecomag_meteo_koef = df_ecomag_meteo_koef['swe'][y_w_1:y_w_2] #Расчет по экомагу на основе COSMO-Ru с поправочным коэффициентом
        
        
        # Данные о приземной температуре воздуха     
        t2m = df_meteostation.iloc[:,6][y_w_1:y_w_2]
        #t2m = t2m.resample('10d').mean()
        #Данные о высоте снежного покрова, см        
        snowe_sd = df_snowe['depth'][y_w_1:y_w_2]
        in_situ_sd = df_in_situ['hSnow'][y_w_1:y_w_2]
        field_sd = df_field_survey['sd'][y_w_1:y_w_2]
        forest_sd = df_forest_survey['sd'][y_w_1:y_w_2]
        
        
        #Блок статистической обработки данных
        
        try:
            
            # Статистическая обработка данных для полевых метеостанций. Подготавка данных
            # версия для полевых станций
            
            df_data_stat = pd.concat([snowe_swe, ecomag_model,ecomag_meteostation, field_in_situ,ecomag_hybrid, ecomag_cosmo_koef, ecomag_meteo_koef], axis = 1) 
            df_data_stat.columns = ['snowe_swe','ecomag_model','ecomag_meteo','field','ecomag_hybrid', 'ecomag_cosmo_koef','ecomag_meteo_koef'] 
            df_data_stat = df_data_stat[np.isfinite(df_data_stat['field'])] # чистим пропуски по полю field
            
            # версия для лесных станций
            #df_data_stat = pd.concat([snowe_swe, ecomag_model,ecomag_meteostation, forest_in_situ,ecomag_hybrid, ecomag_cosmo_koef, ecomag_meteo_koef ], axis = 1) 
            #df_data_stat.columns = ['snowe_swe','ecomag_model','ecomag_meteo','forest','ecomag_hybrid', 'ecomag_cosmo_koef','ecomag_meteo_koef'] 
            #df_data_stat = df_data_stat[np.isfinite(df_data_stat['forest'])] # чистим пропуски по полю field            
            
            
            
            df_data_stat = df_data_stat.dropna(axis = 'rows',thresh = 3) # чистим строкиб где осталось больше 3 пропусков
            #df_data_stat = (df_data_stat [df_data_stat[['field','forest']].notnull().all(1)]) #работает
            
            
            #Статистическая обработка
            
            snowe_1 = df_data_stat.iloc[:,0]
            field_1 = df_data_stat.iloc[:,3]
            #index_1 = df.iloc[:,0]
            
            
            #версия для полевых станций
            
            delta_snowe = df_data_stat['snowe_swe']-df_data_stat['field']
            delta_eco_model = df_data_stat['ecomag_model']-df_data_stat['field']
            delta_eco_meteo = df_data_stat['ecomag_meteo']-df_data_stat['field']
            delta_eco_hybrid = df_data_stat['ecomag_hybrid']-df_data_stat['field']
            delta_eco_cosmo_koef = df_data_stat['ecomag_cosmo_koef']-df_data_stat['field']
            delta_eco_meteo_koef = df_data_stat['ecomag_meteo_koef']-df_data_stat['field']
            
            
            #версия для лесных станций
            #delta_snowe = df_data_stat['snowe_swe']-df_data_stat['forest']
            #delta_eco_model = df_data_stat['ecomag_model']-df_data_stat['forest']
            #delta_eco_meteo = df_data_stat['ecomag_meteo']-df_data_stat['forest']            
            #delta_eco_hybrid = df_data_stat['ecomag_hybrid']-df_data_stat['forest']
            #delta_eco_cosmo_koef = df_data_stat['ecomag_cosmo_koef']-df_data_stat['forest']
            #delta_eco_meteo_koef = df_data_stat['ecomag_meteo_koef']-df_data_stat['forest']
            
            
            #Расчет среднего
            mean_snowe = delta_snowe.mean()
            mean_eco_model = delta_eco_model.mean()
            mean_eco_meteo = delta_eco_meteo.mean()
            mean_eco_hybrid = delta_eco_hybrid.mean()
            mean_eco_cosmo_koef = delta_eco_cosmo_koef.mean()
            mean_eco_meteo_koef = delta_eco_meteo_koef.mean()
            
            #Расчет СКО
            std_snowe = delta_snowe.std()
            std_eco_model = delta_eco_model.std()
            std_eco_meteo = delta_eco_meteo.std()
            std_eco_hybrid = delta_eco_hybrid.std()
            std_eco_cosmo_koef = delta_eco_cosmo_koef.std()
            std_eco_meteo_koef = delta_eco_meteo_koef.std()
            
            #Расчет mae
            # Расчет mae для SnoWE
            try:
                mae_snowe = (sum(abs(delta_snowe)))/len(delta_snowe)        
            except ZeroDivisionError:
                mae_snowe = 0
            # Расчет mae для Ecomag_COSMO
            try:
                mae_eco_model = (sum(abs(delta_eco_model)))/len(delta_eco_model)        
            except ZeroDivisionError:
                mae_eco_model = 0                        
            # Расчет mae для Ecomag_Meteo
            try:
                mae_eco_meteo = (sum(abs(delta_eco_meteo)))/len(delta_eco_meteo)        
            except ZeroDivisionError:
                mae_eco_meteo = 0       
                
            # Расчет mae для Ecomag_hybrid
            try:
                mae_eco_hybrid = (sum(abs(delta_eco_hybrid)))/len(delta_eco_hybrid)        
            except ZeroDivisionError:
                mae_eco_hybrid = 0             
            
            # Расчет mae для Ecomag_COSMO поправочный коэффициент
            try:
                mae_eco_cosmo_koef = (sum(abs(delta_eco_cosmo_koef)))/len(delta_eco_cosmo_koef)        
            except ZeroDivisionError:
                mae_eco_cosmo_koef = 0  
                
            # Расчет mae для Ecomag станции с поправочным коэффициентом
            try:
                mae_eco_meteo_koef = (sum(abs(delta_eco_meteo_koef)))/len(delta_eco_meteo_koef)        
            except ZeroDivisionError:
                mae_eco_meteo_koef = 0  
            
            
            #Расчет rmse
            #Расчет rmse для SnoWE
            try:
                rmse_snowe = math.sqrt(sum(delta_snowe*delta_snowe)/len(delta_snowe))
            except ZeroDivisionError:
                rmse_snowe = 0  
            #Расчет rmse для ECOMAG_model
            try:
                rmse_eco_model = math.sqrt(sum(delta_eco_model*delta_eco_model)/len(delta_eco_model))
            except ZeroDivisionError:
                rmse_eco_model = 0           
            #Расчет rmse для ECOMAG_meteo
            try:
                rmse_eco_meteo = math.sqrt(sum(delta_eco_meteo*delta_eco_meteo)/len(delta_eco_meteo))
            except ZeroDivisionError:
                rmse_eco_meteo = 0            

            #Расчет rmse для ECOMAG_hybrid
            try:
                rmse_eco_hybrid = math.sqrt(sum(delta_eco_hybrid*delta_eco_hybrid)/len(delta_eco_hybrid))
            except ZeroDivisionError:
                rmse_eco_hybrid = 0  

            #Расчет rmse для ECOMAG cosmo версия для модели с коэффициентами
            try:
                rmse_eco_cosmo_koef = math.sqrt(sum(delta_eco_cosmo_koef*delta_eco_cosmo_koef)/len(delta_eco_cosmo_koef))
            except ZeroDivisionError:
                rmse_eco_cosmo_koef = 0

            #Расчет rmse для ECOMAG in-situ версия для модели с коэффициентами 
            try:
                rmse_eco_meteo_koef = math.sqrt(sum(delta_eco_meteo_koef*delta_eco_meteo_koef)/len(delta_eco_meteo_koef))
            except ZeroDivisionError:
                rmse_eco_meteo_koef = 0 







            #Считаем процент улучшений для mae
            # Для модели SnoWE, ECOMAG метео - взят за идеал
            try:
                snowe_mae_result = 100 - ((mae_snowe/mae_eco_meteo)*100)
            except ZeroDivisionError:
                snowe_mae_result = 0             
            # Для модели COSMO, ECOMAG метео - взят за идеал
            try:
                ecomag_mae_result = 100 - ((mae_eco_model/mae_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_mae_result = 0    
            # Для ecomag_meteo, ECOMAG метео - взят за идеал
            try:
                ecomag_met_mae_result = 100 - ((mae_eco_meteo/mae_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_met_mae_result = 0             
            
            # Для ecomag_hybrid, ECOMAG метео - взят за идеал
            try:
                ecomag_hyb_mae_result = 100 - ((mae_eco_hybrid/mae_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_hyb_mae_result = 0  

            # Для ecomag_COSMO koef, ECOMAG метео - взят за идеал
            try:
                ecomag_cosmo_koef_mae_result = 100 - ((mae_eco_cosmo_koef/mae_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_cosmo_koef_mae_result = 0  

            # Для ecomag_meteo koef, ECOMAG метео - взят за идеал
            try:
                ecomag_meteo_koef_mae_result = 100 - ((mae_eco_meteo_koef/mae_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_meteo_koef_mae_result = 0  




            #Считаем процент улучшений для rmse
            # Для модели SnoWE, ECOMAG метео - взят за идеал
            try:
                snowe_rmse_result = 100 - ((rmse_snowe/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                snowe_rmse_result = 0             
            # Для модели COSMO, ECOMAG метео - взят за идеал
            try:
                ecomag_rmse_result = 100 - ((rmse_eco_model/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_rmse_result = 0 

            # Для модели COSMO, ECOMAG метео - взят за идеал
            try:
                ecomag_met_rmse_result = 100 - ((rmse_eco_meteo/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_met_rmse_result = 0
            
            # Для модели ecomag_hybrid, ECOMAG метео - взят за идеал
            try:
                ecomag_hyb_rmse_result = 100 - ((rmse_eco_hybrid/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_hyb_rmse_result = 0

            # Для модели ecomag_cosmo koef, ECOMAG метео - взят за идеал
            try:
                ecomag_cosmo_koef_rmse_result = 100 - ((rmse_eco_cosmo_koef/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_cosmo_koef_rmse_result = 0

            # Для модели ecomag_meteo koef, ECOMAG метео - взят за идеал
            try:
                ecomag_meteo_koef_rmse_result = 100 - ((rmse_eco_meteo_koef/rmse_eco_meteo)*100)
            except ZeroDivisionError:
                ecomag_meteo_koef_rmse_result = 0

            df_st = pd.DataFrame({"SnoWE":[std_snowe,mae_snowe, rmse_snowe,snowe_mae_result, snowe_rmse_result],
                                  "ECOMAG_COSMO":[std_eco_model, mae_eco_model, rmse_eco_model,ecomag_mae_result, ecomag_rmse_result],
                                  #"ECOMAG_hybrid":[std_eco_hybrid, mae_eco_hybrid, rmse_eco_hybrid, ecomag_hyb_mae_result, ecomag_hyb_rmse_result],
                                  "ECOMAG_COSMO_koef":[std_eco_cosmo_koef, mae_eco_cosmo_koef, rmse_eco_cosmo_koef, ecomag_cosmo_koef_mae_result, ecomag_cosmo_koef_rmse_result],
                                  "ECOMAG_meteo_koef":[std_eco_meteo_koef, mae_eco_meteo_koef, rmse_eco_meteo_koef, ecomag_meteo_koef_mae_result, ecomag_meteo_koef_rmse_result],
                                  "ECOMAG_meteo":[std_eco_meteo, mae_eco_meteo, rmse_eco_meteo,ecomag_met_mae_result, ecomag_met_rmse_result]},
                                   index = ["std","mae","rmse","% mae", "% rmse"])


            
            
            df_st.to_csv(result_data_stat + fileName_1[0:5] + ' time_{}_{}.csv'.format(y_w_1,y_w_2), sep=';', float_format='%.3f')
                        #header = ['snowe','eco_model','eco_stat','field'], index_label = 'Date')
            
            
        except NameError as error:
            print ('Exception: ', error)
        
               
        
        
        #блок расчета поправочных коэффициентов
        """
        try:
             
            #k_model = snowe_swe/ecomag_model #Поправочный коэффициент для модели COSMO-Ru (глобальной)
            #k_in_situ = snowe_swe/ecomag_meteostation #Поправочный коэффициент для ecomag счет по станциям
            #df_data_koef = pd.concat([k_model, k_in_situ,t2m], axis = 1)
            #df_data_koef.columns = ['k_eco_cosmo','k_eco_meteo','t2m']
            
             
            #df_data_koef = df_data_stat[np.isfinite(df_data_stat['t2m'])] # чистим пропуски по полю field            
            
            
            
            
            time_step = ['2013-10-10','2013-10-20','2013-10-31','2013-11-10','2013-11-20','2013-11-30','2013-12-10','2013-12-20','2013-12-31','2014-01-10','2014-01-20','2014-01-31',
                         '2014-02-10','2014-02-20','2014-02-28','2014-03-10','2014-03-20','2014-03-31','2014-04-10','2014-04-20','2014-04-30','2014-05-10','2014-05-20','2014-05-31',
                         '2014-10-10','2014-10-20','2014-10-31','2014-11-10','2014-11-20','2014-11-30','2014-12-10','2014-12-20','2014-12-31','2015-01-10','2015-01-20','2015-01-31',
                         '2015-02-10','2015-02-20','2015-02-28','2015-03-10','2015-03-20','2015-03-31','2015-04-10','2015-04-20','2015-04-30','2015-05-10','2015-05-20','2015-05-31',
                         '2015-10-10','2015-10-20','2015-10-31','2015-11-10','2015-11-20','2015-11-30','2015-12-10','2015-12-20','2015-12-31','2016-01-10','2016-01-20','2016-01-31',
                         '2016-02-10','2016-02-20','2016-02-29','2016-03-10','2016-03-20','2016-03-31','2016-04-10','2016-04-20','2016-04-30','2016-05-10','2016-05-20','2016-05-31',
                         '2016-10-10','2016-10-20','2016-10-31','2016-11-10','2016-11-20','2016-11-30','2016-12-10','2016-12-20','2016-12-31','2017-01-10','2017-01-20','2017-01-31',
                         '2017-02-10','2017-02-20','2017-02-28','2017-03-10','2017-03-20','2017-03-31','2017-04-10','2017-04-20','2017-04-30','2017-05-10','2017-05-20','2017-05-31',
                         '2017-10-10','2017-10-20','2017-10-31','2017-11-10','2017-11-20','2017-11-30','2017-12-10','2017-12-20','2017-12-31','2018-01-10','2018-01-20','2018-01-31',
                         '2018-02-10','2018-02-20','2018-02-28','2018-03-10','2018-03-20','2018-03-31','2018-04-10','2018-04-20','2018-04-30','2018-05-10','2018-05-20','2018-05-31']
                        #'2018-10-10','2018-10-20','2018-10-31','2018-11-10','2018-11-20','2018-11-30','2018-12-09','2018-12-20','2018-12-31','2019-01-10','2019-01-20','2019-01-31',
                        #'2019-02-10','2019-02-20','2019-02-28','2019-03-10','2019-03-20','2019-03-31','2019-04-10','2019-04-20','2019-04-30','2019-05-10','2019-05-20','2019-05-31']

            #dtime = pd.to_datetime(time_step, format = '%Y-%m-%d')

            #k_model = snowe_swe/ecomag_model #Поправочный коэффициент для модели COSMO-Ru (глобальной)
            #k_in_situ = snowe_swe/ecomag_meteostation #Поправочный коэффициент для ecomag счет по станциям
            
            k_model = ecomag_model/snowe_swe #Поправочный коэффициент для модели COSMO-Ru (глобальной)
            k_in_situ = ecomag_meteostation/snowe_swe #Поправочный коэффициент для ecomag счет по станциям      
            
            #ts_k_model = pd.Series(k_model, index = dtime)
            #ts_k_in_situ = pd.Series(k_in_situ, index = dtime)
            #ts_t2m = pd.Series(t2m, index = dtime)
            
            
            df_data_koef = pd.concat([k_model, k_in_situ,t2m], axis = 1)
            df_data_koef.columns = ['k_eco_cosmo','k_eco_meteo','t2m']
            
            #df_data_stat = df_data_stat.dropna(axis = 'rows',thresh = 3) # чистим строкиб где осталось больше 3 пропусков
            #df_data_stat = (df_data_stat [df_data_stat[['field','forest']].notnull().all(1)]) #работает            
            
            
            
            df_data_koef.to_csv(result_data + fileName_1[0:5] + ' time_{}_{}.csv'.format(y_w_1,y_w_2), sep=';', float_format='%.3f',
                                header = ['k_eco_cosmo','k_eco_meteo','t2m'], index_label = 'Date')
        except NameError as error:
            print ('Exception: ', error)
        """   
      
        #Блок визуализации результатов
        """
        #График для сравнения запаса воды в снеге 
        fig = plt.figure(figsize = (14,10))
        ax = fig.add_subplot(111)
        nam_1 = u'График сравнения запаса воды в снеге'
        nam_2 = u'Запас воды в снеге, мм'
        l_p = 'upper left'
        try:
            #swe_plot = plot_7(ax, snowe_swe, ecomag_model, ecomag_cosmo_koef, ecomag_meteostation, ecomag_meteo_koef, field_in_situ, forest_in_situ,  nam_1, nam_2, 0, 301, 50, minorLocator_1, l_p, y_w_1, y_w_2) #отрисовка с коэффициентами
            #swe_plot = plot_6(ax, snowe_swe, ecomag_model, ecomag_meteostation, field_in_situ, forest_in_situ, ecomag_hybrid, nam_1, nam_2, 0, 301, 50, minorLocator_1, l_p, y_w_1, y_w_2) #отрисовка гибрида
            swe_plot = plot_5(ax, snowe_swe, ecomag_model, ecomag_meteostation, field_in_situ, forest_in_situ, nam_1, nam_2, 0, 301, 50, minorLocator_1, l_p, y_w_1, y_w_2) #основная версия
            
            plt.savefig(iPath_plot + 'plot_swe_' + fileName_1[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
            plt.gcf().clear()   
        except NameError as error:
            print ( 'Exception: ', error )

                       
        #График для сравнения высоты снежного покрова                   
        fig = plt.figure(figsize = (14,10))
        ax1 = fig.add_subplot(111)              
        name_1 = u'График сравнения высоты снежного покрова'
        name_2 = u'Высота снега, см'
        l_p = 'upper left'
        try:
            sd_plot = plot_4(ax1, snowe_sd, in_situ_sd, field_sd, forest_sd, name_1, name_2, 0, 151, 25, minorLocator_2, l_p, y_w_1, y_w_2)
            #sd_plot = plot_4(ax1, snowe_sd, in_situ_sd, field_sd, name_1, name_2, 0, 151, 25, minorLocator_2, l_p, y_w_1, y_w_2)
            plt.savefig(iPath_plot + 'plot_sd_' + fileName_1[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
            plt.gcf().clear()
        except NameError as error:
            print ( 'Exception: ', error )
        """    
        
        #ax.plot(snowe_swe.index, snowe_swe, color = 'blue', linestyle = '-')
        #ax.plot(ecomag_model.index, ecomag_model, color = 'green', linestyle = '-')
        #ax.plot(ecomag_meteostation.index, ecomag_meteostation, color = 'black', linestyle = '-')
        #ax.scatter(field_in_situ.index, field_in_situ, color = 'red')
        #ax.scatter(forest_in_situ.index, forest_in_situ, color = 'red')
        
        #plt.savefig(iPath_3 + 'plot_1' +'.png', format='png', dpi = 300)
        #plt.savefig(iPath_plot + 'plot_1_' + fileName_1[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
        #plt.gcf().clear()
        
        #fig = plt.figure(figsize = (14,10))
        #ax1 = fig.add_subplot(111)
        #ax1.plot(test_snowe.index, test_snowe, color = 'blue', linestyle = '-')
        #ax1.plot(test.index, test, color = 'green', linestyle = '-')
        #ax1.scatter(test_forest.index, test_forest, color = 'red')
        #ax1.scatter(test_field.index, test_field, color = 'red')
        #plt.savefig(iPath_plot + 'plot_sd_' + fileName_1[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
        #plt.gcf().clear()
