# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:43:16 2019

@author: Evgeny Churiulin
Программа для отрисовки комплексного графика метеопараметров по метеостанциям в бассейне реки Дон.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter
from matplotlib import rcParams

minorLocator_1 = AutoMinorLocator (n=4)
minorFormatter_1 = FormatStrFormatter('%.1f')

minorLocator_2 = AutoMinorLocator (n=4)
minorFormatter_2 = FormatStrFormatter('%.1f')

minorLocator_3 = AutoMinorLocator (n=2)
minorFormatter_3 = FormatStrFormatter('%.1f')

minorLocator_4 = AutoMinorLocator (n=2)
minorFormatter_4 = FormatStrFormatter('%.1f')

minorLocator_5 = AutoMinorLocator (n=2)
minorFormatter_5 = FormatStrFormatter('%.1f')


minorLocator_9 = AutoMinorLocator (n=2)
minorFormatter_9 = FormatStrFormatter('%.1f')

years = mdates.YearLocator() #every year
days = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')

"""
Функция для построения графиков с тремя переменными: Функция строит график ввиде линий
pr_1, pr_2, pr_3 - основные расчетные переменные, далее по ним будет строиться график (нужно чтобы был индекс и значение).
индекс в формате даты с суточной дискретностью
n_1, n_2, n_3 - текст легенды для основных расчетных переменных
n_4 - подпись заголовка для графика
n_5 - подпись оси y
pr_6, pr_7, pr_8 - пределы по шкале y (pr_6 - нижняя отметка, pr_7 - верхняя отметка, pr_8 - шаг)
pr_9 - параметр, вспомогательных делений
l_p - положение легенды
time_step_1,time_step_2 - временной диапазон
"""
def plot_3(ax,pr_1,pr_2,pr_3,n_1, n_2, n_3, n_4, n_5, pr_6, pr_7, pr_8, pr_9, l_p, time_step_1, time_step_2):
    ax.plot(pr_1.index, pr_1, label = n_1, color = 'r', linestyle = '-')
    ax.plot(pr_2.index, pr_2, label = n_2, color = 'm', linestyle = '-')
    ax.plot(pr_3.index, pr_3, label = n_3, color = 'b',  linestyle = '-' )
    ax.set_title(n_4, color = 'black', fontsize = 12, loc = 'right')
    #ax1.text('2016-10-10', 15.0, 'I', fontsize = 20, color= 'r')
    ax.set_ylabel(n_5, color = 'black', fontsize = 14)
    #ax1.tick_params(pad = 10)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_6,pr_7,pr_8))
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
    yax.set_minor_locator(pr_9)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    #plt.savefig(ipath + 'Complex schedule_10_'+ fileName_csv[0:5]+'.png', format='png', dpi = 300)
    #plt.gcf().clear()
"""
Функция для построения графиков с двумя переменными: Функция строит график ввиде линий
pr_1, pr_2 - основные расчетные переменные, далее по ним будет строиться график (нужно чтобы был индекс и значение).
индекс в формате даты с суточной дискретностью
na_1, na_2- текст легенды для основных расчетных переменных
n_3 - подпись заголовка для графика
n_4 - подпись оси y
pr_3, pr_4, pr_5 - пределы по шкале y (pr_6 - нижняя отметка, pr_7 - верхняя отметка, pr_8 - шаг)
pr_6 - параметр вспомогательныъх делений
l_p - положение легенды
time_step_1,time_step_2 - временной диапазон
"""    
def plot_2(ax, pr_1, pr_2, na_1, na_2, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):
    ax.plot(pr_1.index, pr_1, label = na_1, color = 'r', linestyle = '-')
    ax.plot(pr_2.index, pr_2, label = na_2, color = 'b', linestyle = '-')
    ax.set_title(na_3, color = 'black', fontsize = 12, loc = 'right')
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
Функция для построения графика с одной переменной: Функция строит график ввиде линий
pr_1 - основной расчетная переменная, далее по ней будет строиться график (нужно чтобы был индекс и значение).
индекс в формате даты с суточной дискретностью
na_1 - текст легенды для основной расчетной переменной
n_2 - подпись заголовка для графика
n_3 - подпись оси y
pr_2, pr_3, pr_4 - пределы по шкале y (pr_6 - нижняя отметка, pr_7 - верхняя отметка, pr_8 - шаг)
pr_5 - параметр вспомогательныъх делений
l_p - положение легенды
time_step_1,time_step_2 - временной диапазон
"""   

def plot_1(ax, pr_1, nam_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, time_step_1, time_step_2, c):
    ax.plot(pr_1.index, pr_1, label = nam_1, color = c, linestyle = '-')
    ax.set_title(nam_2, color = 'black', fontsize = 12, loc = 'right')
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(nam_3, color = 'black', fontsize = 14)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_2, pr_3, pr_4))
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
    yax.set_minor_locator(pr_5)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    
"""
Функция для построения графика с одной переменной: Функция строит диаграмму
pr_1 - основной расчетная переменная, далее по ней будет строиться график (нужно чтобы был индекс и значение).
индекс в формате даты с суточной дискретностью
na_1 - текст легенды для основной расчетной переменной
n_2 - подпись заголовка для графика
n_3 - подпись оси y
pr_2, pr_3, pr_4 - пределы по шкале y (pr_6 - нижняя отметка, pr_7 - верхняя отметка, pr_8 - шаг)
pr_5 - параметр вспомогательныъх делений
l_p - положение легенды
с - цвет графика
time_step_1, time_step_2 - временной диапазон
"""   
def bar_char_1(bx, pr_1, nam_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, c, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = c)
    bx.set_title(nam_2, color = 'black', fontsize = 12, loc = 'right')
    #ax3.text('2016-10-10', 20.0, 'III', fontsize = 20, color= 'g')
    bx.set_ylabel(nam_3, color = 'black', fontsize = 14)
    bx.get_yticks()
    bx.set_yticks(np.arange(pr_2, pr_3, pr_4))
    bx.legend(loc = l_p, frameon=False)
    bx.get_xticks()
    bx.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    bx.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xbx = bx.xaxis
    ybx = bx.yaxis
    #bx.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    bx.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    bx.xaxis.set_major_formatter(xftm)
    bx.xaxis.set_minor_locator(days)
    for label in bx.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in bx.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    ybx.set_minor_locator(pr_5)
    ybx.set_minor_formatter(NullFormatter())
    xbx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    ybx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    bx.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)  




def bar_char_prec_1(bx, pr_1, prr_2, nam_1, nam_2, nam_3, nam_4, pr_2, pr_3, pr_4, pr_5, l_p, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = 'tab:blue') #твердые осадки
    bx.bar(prr_2.index, prr_2, label = nam_2, color = 'tab:green') #жидкие осадки
    bx.set_title(nam_3, color = 'black', fontsize = 12, loc = 'right')
    #ax3.text('2016-10-10', 20.0, 'III', fontsize = 20, color= 'g')
    bx.set_ylabel(nam_4, color = 'black', fontsize = 14)
    bx.get_yticks()
    bx.set_yticks(np.arange(pr_2, pr_3, pr_4))
    bx.legend(loc = l_p, frameon=False)
    bx.get_xticks()
    bx.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    bx.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xbx = bx.xaxis
    ybx = bx.yaxis
    #bx.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    bx.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    bx.xaxis.set_major_formatter(xftm)
    bx.xaxis.set_minor_locator(days)
    for label in bx.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in bx.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    ybx.set_minor_locator(pr_5)
    ybx.set_minor_formatter(NullFormatter())
    xbx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    ybx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    bx.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)  









def plot_3_snow(ax, prr_1, prr_2, prr_3, name_1, name_2, name_3, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2): # для отрисовки гибрида
    ax.plot(prr_1.index, prr_1, label = name_1, color = 'tab:blue', linestyle = '-') #Для SnoWE
    ax.scatter(prr_2.index, prr_2, label = name_2, color = 'tab:red', marker = '^') #Для полевых снегомерных маршрутов
    ax.scatter(prr_3.index, prr_3, label = name_3, color = 'tab:purple', marker = 'o') #Для лесных снегомерных маршрутов
    ax.set_title(na_3, color = 'black', fontsize = 12, loc = 'right')
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










def bar_char_2(bx, pr_1, prr_1, nam_1, name_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, c, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = c)
    bx.plot(prr_1.index, prr_1, label = name_1, color = 'tab:red', linestyle = '-', linewidth = 2.5)
    
    bx.set_title(nam_2, color = 'black', fontsize = 12, loc = 'right')
    #ax3.text('2016-10-10', 20.0, 'III', fontsize = 20, color= 'g')
    bx.set_ylabel(nam_3, color = 'black', fontsize = 14)
    bx.get_yticks()
    bx.set_yticks(np.arange(pr_2, pr_3, pr_4))
    bx.legend(loc = l_p, frameon=False)
    bx.get_xticks()
    bx.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    bx.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xbx = bx.xaxis
    ybx = bx.yaxis
    #bx.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    bx.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    bx.xaxis.set_major_formatter(xftm)
    bx.xaxis.set_minor_locator(days)
    for label in bx.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in bx.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    ybx.set_minor_locator(pr_5)
    ybx.set_minor_formatter(NullFormatter())
    xbx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    ybx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    bx.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5) 

# Подготовка исходной информации о снежном покрове по данным маршрутных снегомерных наблюдений
"""    
#Подгружаем путь к файлу с маршрутными снегомерными наблюдениями в поле - станции

fileName_field = 'field.csv'
iPath_field = 'D:/Churyulin/DON/result_filter/{}'.format(fileName_field) #основной путь работы
#Путь к папке, где хранятся результаты маршрутных снегомерных наблюдений в поле
path_exit_field = 'D:/Churyulin/DON/snow_survey/field/' #основной путь работы
#Очистка результатов предыдушей работы скрипта
dirs_path_exit_field = os.listdir(path_exit_field) 
for file_field in dirs_path_exit_field:
    os.remove(path_exit_field + file_field)


#Подгружаем путь к файлу с маршрутными снегомерными наблюдениями в лесу
fileName_forest = 'forest.csv'
iPath_forest = 'D:/Churyulin/DON/result_filter/{}'.format(fileName_forest) #основной путь работы
#Путь к папке, где хранятся результаты маршрутных снегомерных наблюдений в лесу
path_exit_forest = 'D:/Churyulin/DON/snow_survey/forest/' #основной путь работы
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

"""











#iPath = 'D:/Churyulin/DON/meteo_in_situ_data_2000_2019/' # путь к данным метеорологических наблюдений SYNOP
iPath = 'D:/Churyulin/DON/test/'
dirs_csv = os.listdir(iPath)

iPath_2 = 'D:/Churyulin/DON/results/all_year_plots/' #Путь к комплексному графику 1 за весь год
dirs_result_year = os.listdir(iPath_2)
for file in dirs_result_year:
    os.remove(iPath_2 + file)

#iPath_complex_1 = 'D:/Churyulin/DON/results/complex_1/'#Путь к комплексному графику за зимний сезон
iPath_complex_1 = 'D:/Churyulin/DON/results/complex_3/'
dirs_result_complex_1 = os.listdir(iPath_complex_1)
#for file in dirs_result_complex_1:
#    os.remove(iPath_complex_1 + file)


#iPath_complex_2 = 'D:/Churyulin/DON/results/complex_2/'
iPath_complex_2 = 'D:/Churyulin/DON/results/complex_4/'
dirs_result_complex_2 = os.listdir(iPath_complex_2)
#for file in dirs_result_complex_2:
#    os.remove(iPath_complex_2 + file)
    

iPath_field = 'D:/Churyulin/DON/snow_survey/field/' # Путь к данным для метеостанции (полевой маршрут)
dirs_field_csv = os.listdir(iPath_field)

iPath_forest = 'D:/Churyulin/DON/snow_survey/forest/' #Путь к данных для метеостанции (лесной маршрут)
dirs_forest_csv = os.listdir(iPath_forest)    

iPath_max_snow = 'D:/Churyulin/DON/results/max_snow_values/'

#iPath_snowe = 'D:/Churyulin/DON/snowe_data/'
iPath_snowe = 'D:/Churyulin/DON/test_snowe/'
dirs_snowe_csv = os.listdir(iPath_snowe)  

data_max_swe = []
data_max_sd = []
data_max_sd_st = []
date = []
index_station = []

ocadki_dek_12 = [] # Список для суммы осадков за декаду
ocadki_sez_12 = [] # Список для суммы осадков за сезон
t_start_list = []  # Список для даты начала декады
t_stop_list = [] #Список для даты конца декады
for file in sorted(dirs_csv):
    try:
        try:
            fileName_csv = file
            #fileName_snowe = '000' + str(file[0:5]) + '.txt'
            fileName_snowe = '000' + str(file[0:5]) + '.csv' #для среднего по водосбору
            iPath_csv = (iPath + fileName_csv) 
            iPath_field_csv = (iPath_field + file)
            iPath_forest_csv = (iPath_forest + file)
            
            iPath_snowe_csv = (iPath_snowe + fileName_snowe)
        
            #Чтение csv и выкидка не нужных значенией (на основе данных Synop)
            df = pd.read_csv(iPath_csv, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                             skipinitialspace = True, na_values= [' ','9990','********'])
            
            #df_snowe = pd.read_csv(iPath_snowe_csv, skiprows = 0, sep=' ', dayfirst = True, parse_dates = True, index_col = [0],
            #                       skipinitialspace = True, na_values= ['9990','********'])
            
            df_snowe = pd.read_csv(iPath_snowe_csv, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],  
                                   skipinitialspace = True, na_values= ['9990','********']) #для среднего по водосбору
            
            #df_snowe= df_snowe.drop_duplicates()
            #Чтение данных для полевого маршрута
            df_field_survey = pd.read_csv(iPath_field_csv, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                          skipinitialspace = True, na_values= ['9990','********']) 
        
            #Чтение данных для лесного маршрута
            df_forest_survey = pd.read_csv(iPath_forest_csv, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0], 
                                           skipinitialspace = True, na_values= ['9990','********'])
        
        except FileNotFoundError as error:
            print ( 'Exception: ', error ) 
        
        
        print ('Columns:', df.columns)
        #Работа с формой для комплексного графика
        rcParams['figure.subplot.left'] = 0.1  # Левая граница
        rcParams['figure.subplot.right']= 0.95  # Правая граница
        rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
        rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
        rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots
            
        w = 19
        periods_winter = [['2000-10-01','2001-05-31'],
                          ['2001-10-01','2002-05-31'],
                          ['2002-10-01','2003-05-31'],
                          ['2003-10-01','2004-05-31'],
                          ['2004-10-01','2005-05-31'],
                          ['2005-10-01','2006-05-31'],
                          ['2006-10-01','2007-05-31'],
                          ['2007-10-01','2008-05-31'],
                          ['2008-10-01','2009-05-31'],
                          ['2009-10-01','2010-05-31'],
                          ['2010-10-01','2011-05-31'],
                          ['2011-10-01','2012-05-31'],
                          ['2012-10-01','2013-05-31'],
                          ['2013-10-01','2014-05-31'],
                          ['2014-10-01','2015-05-31'],
                          ['2015-10-01','2016-05-31'],
                          ['2016-10-01','2017-05-31'],
                          ['2017-10-01','2018-05-31'],
                          ['2018-10-01','2019-05-31']]
                          
                
        #w = 2  
        #periods_winter = [['2018-09-01','2019-05-31']]
        
        """
        w = 7  
        periods_winter = [['2011-01-01','2011-12-31'],
                          ['2012-01-01','2013-12-31'],
                          ['2013-01-01','2014-12-31'],
                          ['2014-01-01','2015-12-31'],
                          ['2015-01-01','2016-12-31'],
                          ['2016-01-01','2017-12-31'],
                          ['2017-01-01','2018-12-31']]
        """
        """
        w = 189
        
        periods_winter = [['2011-09-01','2011-09-10'],
                          ['2011-09-11','2011-09-20'],
                          ['2011-09-21','2011-09-30'],
                          ['2011-10-01','2011-10-10'],
                          ['2011-10-11','2011-10-20'],
                          ['2011-10-21','2011-10-31'],
                          ['2011-11-01','2011-11-10'],
                          ['2011-11-11','2011-11-20'],
                          ['2011-11-21','2011-11-30'],
                          ['2011-12-01','2011-12-10'],
                          ['2011-12-11','2011-12-20'],
                          ['2011-12-21','2011-12-31'],
                          ['2012-01-01','2012-01-10'],
                          ['2012-01-11','2012-01-20'],
                          ['2012-01-21','2012-01-31'],
                          ['2012-02-01','2012-02-10'],
                          ['2012-02-11','2012-02-20'],
                          ['2012-02-21','2012-02-29'],
                          ['2012-03-01','2012-03-10'],
                          ['2012-03-11','2012-03-20'],
                          ['2012-03-21','2012-03-31'],
                          ['2012-04-01','2012-04-10'],
                          ['2012-04-11','2012-04-20'],
                          ['2012-04-21','2012-04-30'],
                          ['2012-05-01','2012-05-10'],
                          ['2012-05-11','2012-05-20'],
                          ['2012-05-21','2012-05-31'],

                          ['2012-09-01','2012-09-10'],
                          ['2012-09-11','2012-09-20'],
                          ['2012-09-21','2012-09-30'],
                          ['2012-10-01','2012-10-10'],
                          ['2012-10-11','2012-10-20'],
                          ['2012-10-21','2012-10-31'],
                          ['2012-11-01','2012-11-10'],
                          ['2012-11-11','2012-11-20'],
                          ['2012-11-21','2012-11-30'],
                          ['2012-12-01','2012-12-10'],
                          ['2012-12-11','2012-12-20'],
                          ['2012-12-21','2012-12-31'],
                          ['2013-01-01','2013-01-10'],
                          ['2013-01-11','2013-01-20'],
                          ['2013-01-21','2013-01-31'],
                          ['2013-02-01','2013-02-10'],
                          ['2013-02-11','2013-02-20'],
                          ['2013-02-21','2013-02-28'],
                          ['2013-03-01','2013-03-10'],
                          ['2013-03-11','2013-03-20'],
                          ['2013-03-21','2013-03-31'],
                          ['2013-04-01','2013-04-10'],
                          ['2013-04-11','2013-04-20'],
                          ['2013-04-21','2013-04-30'],
                          ['2013-05-01','2013-05-10'],
                          ['2013-05-11','2013-05-20'],
                          ['2013-05-21','2013-05-31'],
                                                    
                          ['2013-09-01','2013-09-10'],
                          ['2013-09-11','2013-09-20'],
                          ['2013-09-21','2013-09-30'],
                          ['2013-10-01','2013-10-10'],
                          ['2013-10-11','2013-10-20'],
                          ['2013-10-21','2013-10-31'],
                          ['2013-11-01','2013-11-10'],
                          ['2013-11-11','2013-11-20'],
                          ['2013-11-21','2013-11-30'],
                          ['2013-12-01','2013-12-10'],
                          ['2013-12-11','2013-12-20'],
                          ['2013-12-21','2013-12-31'],
                          ['2014-01-01','2014-01-10'],
                          ['2014-01-11','2014-01-20'],
                          ['2014-01-21','2014-01-31'],
                          ['2014-02-01','2014-02-10'],
                          ['2014-02-11','2014-02-20'],
                          ['2014-02-21','2014-02-28'],
                          ['2014-03-01','2014-03-10'],
                          ['2014-03-11','2014-03-20'],
                          ['2014-03-21','2014-03-31'],
                          ['2014-04-01','2014-04-10'],
                          ['2014-04-11','2014-04-20'],
                          ['2014-04-21','2014-04-30'],
                          ['2014-05-01','2014-05-10'],
                          ['2014-05-11','2014-05-20'],
                          ['2014-05-21','2014-05-31'],
                                                    
                          ['2014-09-01','2014-09-10'],
                          ['2014-09-11','2014-09-20'],
                          ['2014-09-21','2014-09-30'],
                          ['2014-10-01','2014-10-10'],
                          ['2014-10-11','2014-10-20'],
                          ['2014-10-21','2014-10-31'],
                          ['2014-11-01','2014-11-10'],
                          ['2014-11-11','2014-11-20'],
                          ['2014-11-21','2014-11-30'],
                          ['2014-12-01','2014-12-10'],
                          ['2014-12-11','2014-12-20'],
                          ['2014-12-21','2014-12-31'],
                          ['2015-01-01','2015-01-10'],
                          ['2015-01-11','2015-01-20'],
                          ['2015-01-21','2015-01-31'],
                          ['2015-02-01','2015-02-10'],
                          ['2015-02-11','2015-02-20'],
                          ['2015-02-21','2015-02-28'],
                          ['2015-03-01','2015-03-10'],
                          ['2015-03-11','2015-03-20'],
                          ['2015-03-21','2015-03-31'],
                          ['2015-04-01','2015-04-10'],
                          ['2015-04-11','2015-04-20'],
                          ['2015-04-21','2015-04-30'],
                          ['2015-05-01','2015-05-10'],
                          ['2015-05-11','2015-05-20'],
                          ['2015-05-21','2015-05-31'],                          
                          
                          ['2015-09-01','2015-09-10'],
                          ['2015-09-11','2015-09-20'],
                          ['2015-09-21','2015-09-30'],
                          ['2015-10-01','2015-10-10'],
                          ['2015-10-11','2015-10-20'],
                          ['2015-10-21','2015-10-31'],
                          ['2015-11-01','2015-11-10'],
                          ['2015-11-11','2015-11-20'],
                          ['2015-11-21','2015-11-30'],
                          ['2015-12-01','2015-12-10'],
                          ['2015-12-11','2015-12-20'],
                          ['2015-12-21','2015-12-31'],
                          ['2016-01-01','2016-01-10'],
                          ['2016-01-11','2016-01-20'],
                          ['2016-01-21','2016-01-31'],
                          ['2016-02-01','2016-02-10'],
                          ['2016-02-11','2016-02-20'],
                          ['2016-02-21','2016-02-29'],
                          ['2016-03-01','2016-03-10'],
                          ['2016-03-11','2016-03-20'],
                          ['2016-03-21','2016-03-31'],
                          ['2016-04-01','2016-04-10'],
                          ['2016-04-11','2016-04-20'],
                          ['2016-04-21','2016-04-30'],
                          ['2016-05-01','2016-05-10'],
                          ['2016-05-11','2016-05-20'],
                          ['2016-05-21','2016-05-31'],                          

                          ['2016-09-01','2016-09-10'],
                          ['2016-09-11','2016-09-20'],
                          ['2016-09-21','2016-09-30'],
                          ['2016-10-01','2016-10-10'],
                          ['2016-10-11','2016-10-20'],
                          ['2016-10-21','2016-10-31'],
                          ['2016-11-01','2016-11-10'],
                          ['2016-11-11','2016-11-20'],
                          ['2016-11-21','2016-11-30'],
                          ['2016-12-01','2016-12-10'],
                          ['2016-12-11','2016-12-20'],
                          ['2016-12-21','2016-12-31'],
                          ['2017-01-01','2017-01-10'],
                          ['2017-01-11','2017-01-20'],
                          ['2017-01-21','2017-01-31'],
                          ['2017-02-01','2017-02-10'],
                          ['2017-02-11','2017-02-20'],
                          ['2017-02-21','2017-02-28'],
                          ['2017-03-01','2017-03-10'],
                          ['2017-03-11','2017-03-20'],
                          ['2017-03-21','2017-03-31'],
                          ['2017-04-01','2017-04-10'],
                          ['2017-04-11','2017-04-20'],
                          ['2017-04-21','2017-04-30'],
                          ['2017-05-01','2017-05-10'],
                          ['2017-05-11','2017-05-20'],
                          ['2017-05-21','2017-05-31'],

                          ['2017-09-01','2017-09-10'],
                          ['2017-09-11','2017-09-20'],
                          ['2017-09-21','2017-09-30'],
                          ['2017-10-01','2017-10-10'],
                          ['2017-10-11','2017-10-20'],
                          ['2017-10-21','2017-10-31'],
                          ['2017-11-01','2017-11-10'],
                          ['2017-11-11','2017-11-20'],
                          ['2017-11-21','2017-11-30'],
                          ['2017-12-01','2017-12-10'],
                          ['2017-12-11','2017-12-20'],
                          ['2017-12-21','2017-12-31'],
                          ['2018-01-01','2018-01-10'],
                          ['2018-01-11','2018-01-20'],
                          ['2018-01-21','2018-01-31'],
                          ['2018-02-01','2018-02-10'],
                          ['2018-02-11','2018-02-20'],
                          ['2018-02-21','2018-02-28'],
                          ['2018-03-01','2018-03-10'],
                          ['2018-03-11','2018-03-20'],
                          ['2018-03-21','2018-03-31'],
                          ['2018-04-01','2018-04-10'],
                          ['2018-04-11','2018-04-20'],
                          ['2018-04-21','2018-04-30'],
                          ['2018-05-01','2018-05-10'],
                          ['2018-05-11','2018-05-20'],
                          ['2018-05-21','2018-05-31']]

        """
              

        periods_winter = np.array(periods_winter)
        print (periods_winter)
        for tr in range(w):
            try:
                y_w_1 = periods_winter[tr][0]
                y_w_2 = periods_winter[tr][1]
                ts_index_st = df['index'][y_w_1:y_w_2]
                ts_ps_w = df['ps'][y_w_1:y_w_2]
                ts_pmsl_w = df['pmsl'][y_w_1:y_w_2]
                ts_t2m_w = df['t2m'][y_w_1:y_w_2]
                ts_t2m_w_negative = df['t2m_negative'][y_w_1:y_w_2]
                ts_td2m_w = df['td2m'][y_w_1:y_w_2]
                ts_dd10m_w = df['dd10m'][y_w_1:y_w_2]
                #ts_ff10_w = df['ff10m'][y_w_1:y_w_2] #внимание
                #ts_ff10mean_w = df['ff10mean'][y_w_1:y_w_2] #внимание
                ts_ff10mean_w = df['0'][y_w_1:y_w_2] #внимание
                ts_ff10max_w = df['ff10max'][y_w_1:y_w_2]
                ts_tmin2m_w = df['tMin2m'][y_w_1:y_w_2]
                ts_tmax2m_w = df['tMax2m'][y_w_1:y_w_2]
                ts_tming_w = df['tMinG'][y_w_1:y_w_2]
                ts_R12_w = df['R12'][y_w_1:y_w_2]
                ts_R12_liquid = df['R12_liquid'][y_w_1:y_w_2]
                ts_R12_solid = df['R12_solid'][y_w_1:y_w_2]                
                ts_R24_w = df['R24'][y_w_1:y_w_2]          
                ts_t_g_w = df['t_g'][y_w_1:y_w_2]
                ts_hsnow_w = df['hSnow'][y_w_1:y_w_2]
                
                
                snowe_sd = df_snowe['depth'][y_w_1:y_w_2]
                snowe_swe = df_snowe['swe'][y_w_1:y_w_2] #Данные по модели SnoWE
                snowe_rho = df_snowe['rho'][y_w_1:y_w_2] #Данные по модели SnoWE
                field_in_situ = df_field_survey['swe'][y_w_1:y_w_2] #полевые снегомерные маршруты
                forest_in_situ = df_forest_survey['swe'][y_w_1:y_w_2] #лесные снегомерные маршруты
                
                
                snowe_rho = df_snowe['rho'][y_w_1:y_w_2] #Данные по модели SnoWE
                field_in_situ_rho = df_field_survey['rho'][y_w_1:y_w_2] #полевые снегомерные маршруты
                forest_in_situ_rho = df_forest_survey['rho'][y_w_1:y_w_2] #лесные снегомерные маршруты                
                
                #Блок максимальных значений по модели
                t_start = y_w_1
                t_stop = y_w_2
                
                max_snow_swe = snowe_swe.max()
                max_snow_sd = snowe_sd.max()
                time = snowe_swe.idxmax()
                index_st = ts_index_st.mean()
                max_hsnow_st = ts_hsnow_w.max()
                sum_ocadkov_dek = ts_R12_w.sum()
                
                
                
                data_max_swe.append(max_snow_swe)
                data_max_sd.append(max_snow_sd)
                date.append(time)
                index_station.append(index_st)
                data_max_sd_st.append(max_hsnow_st)
                ocadki_dek_12.append(sum_ocadkov_dek)
                
                
                t_start_list.append(t_start)
                t_stop_list.append(t_stop)
                
                x = pd.Series(data_max_swe, index = date)
                y = pd.Series(index_station, index = date)
                z = pd.Series(data_max_sd, index = date)
                k = pd.Series(data_max_sd_st, index = date)
                sum_ocadkov_za_dekadu = pd.Series(ocadki_dek_12, index = date)
                start_time = pd.Series(t_start_list, index = date)
                stop_time = pd.Series(t_stop_list, index = date)
                
                df_max_snow = pd.concat([y,x,z, sum_ocadkov_za_dekadu, start_time,stop_time],axis = 1)
                
                df_max_snow.columns = ['index','swe','sd', 'Sum_ocadkov','t_start','t_stop']
                
                df_max_snow.to_csv(iPath_max_snow + 'snow_max_dekada' + '.csv', sep=';', float_format='%.3f')
                       
                #header = ['snowe','eco_model','eco_stat','field'], index_label = 'Date')
                #Блок максимальных значений по метеостанциям

                
                
                #data.extend(max_snow)
                #data.append(t)
                #df_st = pd.concat([t,max_snow], axis = 1)      
                
                #df_st = pd.DataFrame({"Values_max":[max_snow],
                #                      "Date":[t]},
                #                       index = ["1"])
                
                #Отрисовка комплексного графика 1
                """
                #Работа с графиком
                #plt.style.use('ggplot')
                fig_w_1 = plt.figure(figsize = (14,10))
                
                #Задание координатной сетки и места где будут располагаться графики
                egrid_w_1 = (4,4)
                w_ax1 = plt.subplot2grid(egrid_w_1, (0,0), colspan = 4)
                w_ax2 = plt.subplot2grid(egrid_w_1, (1,0), colspan = 4)
                w_ax3 = plt.subplot2grid(egrid_w_1, (2,0), colspan = 4)
                w_ax4 = plt.subplot2grid(egrid_w_1, (3,0), colspan = 4)
                
                # График для температура воздуха: t2m - температура воздуха (град С);
                # График для температуры точки росы: td2m - температура точки росы (град С);    
                n_1 = '1' #Средняя температура воздуха
                n_2 = '2'
                n_3 =  u'I' # график для отображения температуры воздуха и температуры точки росы
                n_4 = u'Температура, С'
                l_p = 'lower left'
                #colo_1 = 'r'
                #temperatura = plot_1(w_ax1, ts_t2m_w, n_1, n_2, n_3, -30, 31, 15, minorLocator_1, l_p, y_w_1, y_w_2, colo_1)
                try:
                    temperatura = plot_2(w_ax1, ts_t2m_w, ts_t2m_w_negative, n_1, n_2, n_3, n_4, -30, 31, 15, minorLocator_2, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in temperatura: ', error )
                
                #temperatura = plot_2(w_ax1, ts_tmax2m_w, ts_t2m_w, ts_tmin2m_w, n_1, n_2, n_3, n_4, n_5, -30, 31, 15, minorLocator_1, l_p, y_w_1, y_w_2)                
                
                # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
                #t_g - температура поверхности почвы (град С)       
                na_1 = '3' #температура почвы
                na_2 = '4' #минимальная температура почвы
                na_3 = u'II' # графики для температуры поверхности почвы и минимальной температуры поверхности почвы
                na_4 = u'Температура, С'
                l_p = 'lower left'
                try:
                    soil_temp = plot_2(w_ax2, ts_t_g_w, ts_tming_w, na_1, na_2, na_3, na_4, -30, 31, 15, minorLocator_2, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )
                
                #График для осадков за 24 часа, мм - RAINS
                name_001 = '5' # осадки за 24 часа - твердые
                name_002 = '6' # осадки за 24 часа - жидкие
                name_003 = u'III' # Графики для суммы осадков за 24 часа
                name_004 = u'Осадки, мм' 
                l_p = 'upper left'
                #col = 'g'
                
                up_R12 = 101
                step_R12 = 25
                
                if ts_R12_w.max() > 75 :
                    up_R12 = 101
                    step_R12 = 25
                    
                elif ts_R12_w.max() > 55:
                    up_R12 = 61
                    step_R12 = 15
                else:
                    up_R12 = 41
                    step_R12 = 10
                
                #precipitation_24 = bar_char_1(w_ax3, ts_R12_w, name_001, name_002, name_003, 0, up_R12, step_R12, minorLocator_3, l_p, col, y_w_1, y_w_2)
                try:
                    precipitation_12 = bar_char_prec_1(w_ax3, ts_R12_solid, ts_R12_liquid, name_001, name_002, name_003, name_004, 0, up_R12, step_R12, minorLocator_3, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception R12: ', error )
                    
                      
                    
                #График для высоты снежного покрова, см
                name_0001 = '6' #высота снега
                name_0002 = u'IV' #график для высоты снега
                name_0003 = u'Высота снега, см' 
                l_p = 'upper left'
                colo = 'b'
                up_snow_sd = 101
                step_sd = 25 
                start_sd = 0
                if ts_hsnow_w.max() > 75 :
                    up_snow_sd = 101
                    step_sd = 25
                elif ts_hsnow_w.max() > 55:
                    up_snow_sd = 81
                    step_sd = 20
                else:
                    up_snow_sd = 51
                    step_sd = 10   

                try:
                    snow_24 = bar_char_1(w_ax4, ts_hsnow_w, name_0001, name_0002, name_0003, start_sd, up_snow_sd, step_sd, minorLocator_4, l_p, colo, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception R12: ', error )
                plt.savefig(iPath_complex_1 + 'Complex schedule_1_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
                plt.gcf().clear()
                
                """
                #Отрисовка комплексного графика 2
                
                
                #plt.style.use('ggplot')
                fig_w_2 = plt.figure(figsize = (14,10))
                
                #Задание координатной сетки и места где будут располагаться графики
                egrid_w_2 = (5,4)
                w_bx1 = plt.subplot2grid(egrid_w_2, (0,0), colspan = 4)
                w_bx2 = plt.subplot2grid(egrid_w_2, (1,0), colspan = 4)
                w_bx3 = plt.subplot2grid(egrid_w_2, (2,0), colspan = 4)
                w_bx4 = plt.subplot2grid(egrid_w_2, (3,0), colspan = 4)
                w_bx5 = plt.subplot2grid(egrid_w_2, (4,0), colspan = 4)
                # График для температура воздуха: t2m - температура воздуха (град С);
                # График для температуры точки росы: td2m - температура точки росы (град С);    
                name_1 = '1' #Средняя температура воздуха
                name_2 = '2'
                name_3 =  u'I' # график для отображения температуры воздуха и температуры точки росы
                name_4 = u'Температура, С'
                l_p = 'lower left'
                #colo_1 = 'r'
                #temperatura = plot_1(w_ax1, ts_t2m_w, n_1, n_2, n_3, -30, 31, 15, minorLocator_1, l_p, y_w_1, y_w_2, colo_1)
                try:
                    temperatura = plot_2(w_bx1, ts_t2m_w, ts_t2m_w_negative, name_1, name_2, name_3, name_4, -30, 31, 15, minorLocator_2, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )
                                
                    
                    
                #График для осадков за 24 часа, мм - RAINS
                name_001 = '3' # осадки за 24 часа - твердые
                name_002 = '4' # осадки за 24 часа - жидкие
                name_003 = u'II' # Графики для суммы осадков за 24 часа
                name_004 = u'Осадки, мм' 
                l_p = 'upper left'
                #col = 'g'
                
                up_R12 = 101
                step_R12 = 25
                
                if ts_R12_w.max() > 75 :
                    up_R12 = 101
                    step_R12 = 25
                    
                elif ts_R12_w.max() > 55:
                    up_R12 = 61
                    step_R12 = 15
                else:
                    up_R12 = 41
                    step_R12 = 10
                
                #precipitation_24 = bar_char_1(w_ax3, ts_R12_w, name_001, name_002, name_003, 0, up_R12, step_R12, minorLocator_3, l_p, col, y_w_1, y_w_2)
                try:
                    precipitation_12 = bar_char_prec_1(w_bx2, ts_R12_solid, ts_R12_liquid, name_001, name_002, name_003, name_004, 0, up_R12, step_R12, minorLocator_3, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception R12: ', error )    
                    
                #График для высоты снежного покрова, см
                name_0001 = '6' #высота снега
                name_0002 = u'III' #график для высоты снега
                name_0003 = u'Высота снега, см' 
                name_0004 = '5' #snowe
                l_p = 'upper left'
                colo = 'b'
                up_snow_sd = 101
                step_sd = 25 
                start_sd = 0
                if ts_hsnow_w.max() > 75 :
                    up_snow_sd = 101
                    step_sd = 25
                elif ts_hsnow_w.max() > 55:
                    up_snow_sd = 81
                    step_sd = 20
                else:
                    up_snow_sd = 51
                    step_sd = 10   

                try:
                    snow_24 = bar_char_2(w_bx3, ts_hsnow_w, snowe_sd, name_0001, name_0004, name_0002, name_0003, start_sd, up_snow_sd, step_sd, minorLocator_4, l_p, colo, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )
                
                
                nam_1 = '7' #snowe
                nam_2 = '8' #field snow
                nam_3 = '9' #forest snow
                nam_4 = 'IV' #график для данных snowe
                nam_5 = u'SWE, мм' # запас воды в снеге
                l_p = 'upper left'
                
                up_snow_swe = 251
                step_swe = 50 
                start_swe = 0
                if field_in_situ.max() > 155 :
                    up_snow_swe = 251
                    step_swe = 50
                elif field_in_situ.max() > 105:
                    up_snow_swe = 151
                    step_swe = 25
                elif field_in_situ.max() > 75:
                    up_snow_swe = 101
                    step_swe = 20
                elif field_in_situ.max() > 55:
                    up_snow_swe = 81
                    step_swe = 20                       
                elif field_in_situ.max() > 35:
                    up_snow_swe = 51
                    step_swe = 10                     
                else:
                    up_snow_swe = 31
                    step_swe = 5 

                try:
                    snowe_info = plot_3_snow(w_bx4, snowe_swe, field_in_situ, forest_in_situ, nam_1, nam_2, nam_3, nam_4, nam_5, start_swe, up_snow_swe, step_swe, minorLocator_5, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )

                        
                name_r_1 = '10' #snowe
                name_r_2 = '11' #field snow
                name_r_3 = '12' #forest snow
                name_r_4 = 'V' #график для данных snowe
                name_r_5 = u'Rho, мм' # запас воды в снеге
                l_p = 'upper left'
                    
                up_snow_rho = 701
                step_rho = 100 
                start_rho = 0
                if snowe_rho.max() > 555 :
                    up_snow_rho = 701
                    step_rho = 100
                elif snowe_rho.max() > 405:
                    up_snow_rho = 501
                    step_rho = 50
                elif snowe_rho.max() > 305:
                    up_snow_rho = 401
                    step_rho = 50
                elif snowe_rho.max() > 205:
                    up_snow_rho = 301
                    step_rho = 25                       
                elif snowe_rho.max() > 105:
                    up_snow_rho = 201
                    step_rho = 25                     
                else:
                    up_snow_rho = 101
                    step_rho = 10 
                    
                try:
                    snowe_rho = plot_3_snow(w_bx5, snowe_rho, field_in_situ_rho*1000, forest_in_situ_rho*1000, name_r_1, name_r_2, name_r_3, name_r_4, name_r_5, start_rho, up_snow_rho, step_rho, minorLocator_9, l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )
                                      
                plt.savefig(iPath_complex_2 + 'Complex schedule_2_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
                plt.gcf().clear()                    
                
                                
                
                
               
                
            except ValueError as error:
                print ( 'Exception in plots: ', error )        
    except NameError as error:
        print ( 'Exception in programm: ', error )


