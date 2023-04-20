# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 19:00:56 2018

@author: Evgeny Churiulin
Программа предназначена для одновременной отрисовке данных о снежном покрове в Москве и Москвском регионе
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

minorLocator_3 = AutoMinorLocator (n=4)
minorFormatter_3 = FormatStrFormatter('%.1f')

years = mdates.YearLocator() #every year
days = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')

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
def plot_16(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, prr_7, prr_8, prr_9, prr_10, prr_11, prr_12, prr_13, prr_14, prr_15, prr_16, na_3, na_4, pr_3, pr_4, pr_5, pr_6, time_step_1, time_step_2, left_b, rigth_b):
    """
    ax.plot(prr_1.index, prr_1, label = fileName_1[0:5], color = 'tab:blue', linestyle = '-')
    ax.plot(prr_2.index, prr_2, label = fileName_2[0:5], color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = fileName_3[0:5], color = 'tab:green', linestyle = '-.')
    ax.plot(prr_4.index, prr_4, label = fileName_4[0:5], color = 'tab:red', linestyle = ':')
    ax.plot(prr_5.index, prr_5, label = fileName_5[0:5], color = 'tab:purple', linestyle = '-.')
    ax.plot(prr_6.index, prr_6, label = fileName_6[0:5], color = 'tab:brown', linestyle = '--')
    ax.plot(prr_7.index, prr_7, label = fileName_7[0:5], color = 'tab:pink', linestyle = '-')
    ax.plot(prr_8.index, prr_8, label = fileName_8[0:5], color = 'tab:gray', linestyle = '--')
    ax.plot(prr_9.index, prr_9, label = fileName_9[0:5], color = 'tab:olive', linestyle = '-.')
    ax.plot(prr_10.index, prr_10, label = fileName_10[0:5], color = 'tab:cyan', linestyle = ':')
    ax.plot(prr_11.index, prr_11, label = fileName_11[0:5], color = 'tab:brown', linestyle = '-.')
    ax.plot(prr_12.index, prr_12, label = fileName_12[0:5], color = 'maroon', linestyle = '--')
    #ax.plot(prr_12.index, prr_12, label = fileName_12[0:5], color = 'tab:magenta', linestyle = '--')
    ax.plot(prr_13.index, prr_13, label = fileName_13[0:5], color = 'lavender', linestyle = '-')
    ax.plot(prr_14.index, prr_14, label = fileName_14[0:5], color = 'lightgreen', linestyle = '--')
    ax.plot(prr_15.index, prr_15, label = fileName_15[0:5], color = 'lime', linestyle = '-.')
    ax.plot(prr_16.index, prr_16, label = fileName_16[0:5], color = 'salmon', linestyle = ':')
    """
    ax.plot(prr_1.index, prr_1, color = 'tab:blue', linestyle = '-')
    ax.plot(prr_2.index, prr_2, color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, color = 'tab:green', linestyle = '-.')
    ax.plot(prr_4.index, prr_4, color = 'tab:red', linestyle = ':')
    ax.plot(prr_5.index, prr_5, color = 'tab:purple', linestyle = '-.')
    ax.plot(prr_6.index, prr_6, color = 'tab:brown', linestyle = '--')
    ax.plot(prr_7.index, prr_7, color = 'tab:pink', linestyle = '-')
    ax.plot(prr_8.index, prr_8, color = 'tab:gray', linestyle = '--')
    ax.plot(prr_9.index, prr_9, color = 'tab:olive', linestyle = '-.')
    ax.plot(prr_10.index, prr_10, color = 'tab:cyan', linestyle = ':')
    ax.plot(prr_11.index, prr_11, color = 'tab:brown', linestyle = '-.')
    ax.plot(prr_12.index, prr_12, color = 'maroon', linestyle = '--')
    #ax.plot(prr_12.index, prr_12, label = fileName_12[0:5], color = 'tab:magenta', linestyle = '--')
    ax.plot(prr_13.index, prr_13, color = 'lavender', linestyle = '-')
    ax.plot(prr_14.index, prr_14, color = 'lightgreen', linestyle = '--')
    ax.plot(prr_15.index, prr_15, color = 'lime', linestyle = '-.')
    ax.plot(prr_16.index, prr_16, color = 'salmon', linestyle = ':')
    
    
    ax.set_title(na_3, color = 'black', fontsize = 14)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 14)
    #ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.set_ylim(left_b, rigth_b)
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
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    
    lab1 = fileName_1[0:5]
    lab2 = fileName_2[0:5]
    lab3 = fileName_3[0:5]
    lab4 = fileName_4[0:5]
    lab5 = fileName_5[0:5]
    lab6 = fileName_6[0:5]
    lab7 = fileName_7[0:5]
    lab8 = fileName_8[0:5]
    lab9 = fileName_9[0:5]
    lab10 = fileName_10[0:5]
    lab11 = fileName_11[0:5]
    lab12 = fileName_12[0:5]
    lab13 = fileName_13[0:5]
    lab14 = fileName_14[0:5]
    lab15 = fileName_15[0:5]
    lab16 = fileName_16[0:5]
    
    plt.legend((lab1,lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9, lab10, lab11, lab12, lab13, lab14, lab15, lab16), fontsize = 12, loc = 'upper left', frameon=True )


def plot_11(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, prr_7, prr_8, prr_9, prr_10, prr_11, na_3, na_4, pr_3, pr_4, pr_5, pr_6, time_step_1, time_step_2, left_b, rigth_b):
    """
    ax.plot(prr_1.index, prr_1, label = fileName_1[0:5], color = 'tab:blue', linestyle = '-')
    ax.plot(prr_2.index, prr_2, label = fileName_2[0:5], color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = fileName_3[0:5], color = 'tab:green', linestyle = '-.')
    ax.plot(prr_4.index, prr_4, label = fileName_4[0:5], color = 'tab:red', linestyle = ':')
    ax.plot(prr_5.index, prr_5, label = fileName_5[0:5], color = 'tab:purple', linestyle = '-.')
    ax.plot(prr_6.index, prr_6, label = fileName_6[0:5], color = 'tab:brown', linestyle = '--')
    ax.plot(prr_7.index, prr_7, label = fileName_7[0:5], color = 'tab:pink', linestyle = '-')
    ax.plot(prr_8.index, prr_8, label = fileName_8[0:5], color = 'tab:gray', linestyle = '--')
    ax.plot(prr_9.index, prr_9, label = fileName_9[0:5], color = 'tab:olive', linestyle = '-.')
    ax.plot(prr_10.index, prr_10, label = fileName_10[0:5], color = 'tab:cyan', linestyle = ':')
    ax.plot(prr_11.index, prr_11, label = fileName_11[0:5], color = 'tab:brown', linestyle = '-.')
    ax.plot(prr_12.index, prr_12, label = fileName_12[0:5], color = 'maroon', linestyle = '--')
    #ax.plot(prr_12.index, prr_12, label = fileName_12[0:5], color = 'tab:magenta', linestyle = '--')
    ax.plot(prr_13.index, prr_13, label = fileName_13[0:5], color = 'lavender', linestyle = '-')
    ax.plot(prr_14.index, prr_14, label = fileName_14[0:5], color = 'lightgreen', linestyle = '--')
    ax.plot(prr_15.index, prr_15, label = fileName_15[0:5], color = 'lime', linestyle = '-.')
    ax.plot(prr_16.index, prr_16, label = fileName_16[0:5], color = 'salmon', linestyle = ':')
    """
    ax.plot(prr_1.index, prr_1, color = 'tab:blue', linestyle = '-')
    ax.plot(prr_2.index, prr_2, color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, color = 'tab:green', linestyle = '-.')
    ax.plot(prr_4.index, prr_4, color = 'tab:red', linestyle = ':')
    ax.plot(prr_5.index, prr_5, color = 'tab:purple', linestyle = '-.')
    ax.plot(prr_6.index, prr_6, color = 'tab:brown', linestyle = '--')
    ax.plot(prr_7.index, prr_7, color = 'tab:pink', linestyle = '-')
    ax.plot(prr_8.index, prr_8, color = 'tab:gray', linestyle = '--')
    ax.plot(prr_9.index, prr_9, color = 'tab:olive', linestyle = '-.')
    ax.plot(prr_10.index, prr_10, color = 'tab:cyan', linestyle = ':')
    ax.plot(prr_11.index, prr_11, color = 'tab:brown', linestyle = '-.')
    


    
    ax.set_title(na_3, color = 'black', fontsize = 14)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 14)
    #ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.set_ylim(left_b, rigth_b)
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
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    
    lab1 = fileName_1[0:5]
    lab2 = fileName_2[0:5]
    lab3 = fileName_3[0:5]
    lab4 = fileName_4[0:5]
    lab5 = fileName_5[0:5]
    
    lab7 = fileName_7[0:5]
    lab8 = fileName_8[0:5]
    
    lab10 = fileName_10[0:5]
    
    lab12 = fileName_12[0:5]
    
    lab14 = fileName_14[0:5]
    lab15 = fileName_15[0:5]
    
    
    plt.legend((lab1,lab2, lab3, lab4, lab5, lab7, lab8,lab10, lab12, lab14, lab15), fontsize = 12, loc = 'upper left', frameon=True )



#Версия для работы по одной станции
#fileName = '27515.csv'
#iPath = 'D:/Churyulin/msu_cosmo/Moscow_data/1_day/{}'.format(fileName)
    
fileName_1 = '27417.csv'
fileName_2 = '27419.csv'
fileName_3 = '27502.csv'
fileName_4 = '27509.csv'
fileName_5 = '27511.csv'
fileName_6 = '27515.csv'
fileName_7 = '27523.csv'
fileName_8 = '27538.csv'
fileName_9 = '27605.csv'
fileName_10 = '27611.csv'
fileName_11 = '27612.csv'
fileName_12 = '27618.csv'
fileName_13 = '27619.csv'
fileName_14 = '27625.csv'
fileName_15 = '27627.csv'
fileName_16 = '557375.csv'



iPath_1 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_1) #Москвоские метеорологические станции
iPath_2 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_2)
iPath_3 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_3)
iPath_4 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_4)
iPath_5 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_5)
iPath_6 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_6)
iPath_7 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_7)
iPath_8 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_8)
iPath_9 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_9)
iPath_10 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_10)
iPath_11 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_11)
iPath_12 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_12)
iPath_13 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_13)
iPath_14 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_14)
iPath_15 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_15)
iPath_16 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data/{}'.format(fileName_16)



"""
#Путь к финальному результату (графики с фильтром для зимы)
iPath_3 = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/result/plot1/'
dirs_result_winter = os.listdir(iPath_3)
for file in dirs_result_winter:
    os.remove(iPath_3 + file)
"""
#iPath_result = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/result/plot_1/'
iPath_result = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/result/plot_1/'
dirs_result_winter = os.listdir(iPath_result)
for file in dirs_result_winter:
    os.remove(iPath_result + file)


#Чтение csv и выкидка не нужных значенией
    
df_1 = pd.read_csv(iPath_1, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_2 = pd.read_csv(iPath_2, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_3 = pd.read_csv(iPath_3, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_4 = pd.read_csv(iPath_4, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_5 = pd.read_csv(iPath_5, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_6 = pd.read_csv(iPath_6, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_7 = pd.read_csv(iPath_7, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_8 = pd.read_csv(iPath_8, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_9 = pd.read_csv(iPath_9, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_10 = pd.read_csv(iPath_10, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_11 = pd.read_csv(iPath_11, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_12 = pd.read_csv(iPath_12, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_13 = pd.read_csv(iPath_13, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_14 = pd.read_csv(iPath_14, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_15 = pd.read_csv(iPath_15, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])
df_16 = pd.read_csv(iPath_16, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                   skipinitialspace = True, na_values= ['9990','********'])

#Работа с формой для комплексного графика
rcParams['figure.subplot.left'] = 0.1  # Левая граница
rcParams['figure.subplot.right']= 0.95  # Правая граница
rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots
    
w = 18  
periods_winter = [['2000-10-01','2001-04-30'],
                  ['2001-10-01','2002-04-30'],
                  ['2002-10-01','2003-04-30'],
                  ['2003-10-01','2004-04-30'],
                  ['2004-10-01','2005-04-30'],
                  ['2005-10-01','2006-04-30'],
                  ['2006-10-01','2007-04-30'],
                  ['2007-10-01','2008-04-30'],
                  ['2008-10-01','2009-04-30'],
                  ['2009-10-01','2010-04-30'],
                  ['2010-10-01','2011-04-30'],
                  ['2011-10-01','2012-04-30'],
                  ['2012-10-01','2013-04-30'],
                  ['2013-10-01','2014-04-30'],
                  ['2014-10-01','2015-04-30'],
                  ['2015-10-01','2016-04-30'],
                  ['2016-10-01','2017-04-30'],
                  ['2017-10-01','2018-04-30']]
    
periods_winter = np.array(periods_winter)
print (periods_winter)
for tr in range(w):
    y_w_1 = periods_winter[tr][0]
    y_w_2 = periods_winter[tr][1]
    
    ts_sd_1 = df_1['depth'][y_w_1:y_w_2]
    ts_rho_1 = df_1['rho'][y_w_1:y_w_2]
    ts_swe_1 = df_1['swe'][y_w_1:y_w_2]

    ts_sd_2 = df_2['depth'][y_w_1:y_w_2]
    ts_rho_2 = df_2['rho'][y_w_1:y_w_2]
    ts_swe_2 = df_2['swe'][y_w_1:y_w_2]
    
    ts_sd_3 = df_3['depth'][y_w_1:y_w_2]
    ts_rho_3 = df_3['rho'][y_w_1:y_w_2]
    ts_swe_3 = df_3['swe'][y_w_1:y_w_2]
    
    ts_sd_4 = df_4['depth'][y_w_1:y_w_2]
    ts_rho_4 = df_4['rho'][y_w_1:y_w_2]
    ts_swe_4 = df_4['swe'][y_w_1:y_w_2]
    
    ts_sd_5 = df_5['depth'][y_w_1:y_w_2]
    ts_rho_5 = df_5['rho'][y_w_1:y_w_2]
    ts_swe_5 = df_5['swe'][y_w_1:y_w_2]
    
    ts_sd_6 = df_6['depth'][y_w_1:y_w_2]
    ts_rho_6 = df_6['rho'][y_w_1:y_w_2]
    ts_swe_6 = df_6['swe'][y_w_1:y_w_2]
    
    ts_sd_7 = df_7['depth'][y_w_1:y_w_2]
    ts_rho_7 = df_7['rho'][y_w_1:y_w_2]
    ts_swe_7 = df_7['swe'][y_w_1:y_w_2]
    
    ts_sd_8 = df_8['depth'][y_w_1:y_w_2]
    ts_rho_8 = df_8['rho'][y_w_1:y_w_2]
    ts_swe_8 = df_8['swe'][y_w_1:y_w_2]
    
    ts_sd_9 = df_9['depth'][y_w_1:y_w_2]
    ts_rho_9 = df_9['rho'][y_w_1:y_w_2]
    ts_swe_9 = df_9['swe'][y_w_1:y_w_2]
    
    ts_sd_10 = df_10['depth'][y_w_1:y_w_2]
    ts_rho_10 = df_10['rho'][y_w_1:y_w_2]
    ts_swe_10 = df_10['swe'][y_w_1:y_w_2]
    
    ts_sd_11 = df_11['depth'][y_w_1:y_w_2]
    ts_rho_11 = df_11['rho'][y_w_1:y_w_2]
    ts_swe_11 = df_11['swe'][y_w_1:y_w_2]
    
    ts_sd_12 = df_12['depth'][y_w_1:y_w_2]
    ts_rho_12 = df_12['rho'][y_w_1:y_w_2]
    ts_swe_12 = df_12['swe'][y_w_1:y_w_2]
    
    ts_sd_13 = df_13['depth'][y_w_1:y_w_2]
    ts_rho_13 = df_13['rho'][y_w_1:y_w_2]
    ts_swe_13 = df_13['swe'][y_w_1:y_w_2]
    
    ts_sd_14 = df_14['depth'][y_w_1:y_w_2]
    ts_rho_14 = df_14['rho'][y_w_1:y_w_2]
    ts_swe_14 = df_14['swe'][y_w_1:y_w_2]
    
    ts_sd_15 = df_15['depth'][y_w_1:y_w_2]
    ts_rho_15 = df_15['rho'][y_w_1:y_w_2]
    ts_swe_15 = df_15['swe'][y_w_1:y_w_2]
    
    ts_sd_16 = df_16['depth'][y_w_1:y_w_2]
    ts_rho_16 = df_16['rho'][y_w_1:y_w_2]
    ts_swe_16 = df_16['swe'][y_w_1:y_w_2]
    
    #Работа с графиком
    #plt.style.use('ggplot')
    
    #ts_swe_max_1 = ts_swe_16.max()
    #print (ts_swe_max_1)
    
    #ts_swe_mean_1 = ts_swe_16.mean()
    #print (ts_swe_mean_1)
    
    
    fig_w_1 = plt.figure(figsize = (14,10))
    
    
    #Задание координатной сетки и места где будут располагаться графики
    #egrid_w_1 = (1,4)
    #w_ax1 = plt.subplot2grid(egrid_w_1, (0,0), colspan = 4)
    w_ax1 = fig_w_1.add_subplot(111)
    
    
    #w_ax2 = plt.subplot2grid(egrid_w_1, (1,0), colspan = 4)
    #w_ax3 = plt.subplot2grid(egrid_w_1, (2,0), colspan = 4)
        
        
    nam_2 = u'Высота снега'
    nam_3 = u'Высота снега, см'
    #l_p = 'upper left'
    #colo_1 = 'g'
    sd = plot_16(w_ax1, ts_sd_1, ts_sd_2, ts_sd_3, ts_sd_4, ts_sd_5, ts_sd_6, ts_sd_7, ts_sd_8, ts_sd_9, ts_sd_10, ts_sd_11, ts_sd_12, ts_sd_13, ts_sd_14, ts_sd_15, ts_sd_16, nam_2, nam_3, 0, 81, 10, minorLocator_1, y_w_1, y_w_2, 0, 80)
    #sd = plot_11(w_ax1, ts_sd_1, ts_sd_2, ts_sd_3, ts_sd_4, ts_sd_5, ts_sd_7, ts_sd_8, ts_sd_10, ts_sd_12, ts_sd_14, ts_sd_15, nam_2, nam_3, 0, 81, 10, minorLocator_1, y_w_1, y_w_2, 0, 80)
    #sd = plot_5(w_ax1, ts_sd_6, ts_sd_9,ts_sd_11, ts_sd_13, ts_sd_16, nam_2, nam_3, 0, 81, 10, minorLocator_1, y_w_1, y_w_2, 0, 80)
    plt.savefig(iPath_result + 'SD_'+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
    #plot_16(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, prr_7, prr_8, prr_9, prr_10, prr_11, prr_12, prr_13, prr_14, prr_15, prr_16, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):
    #dew_point = plot_1(w_ax1, ts_sd, nam_1, nam_2, nam_3, 0, 51, 10, minorLocator_1, l_p, y_w_1, y_w_2, colo_1)
        
    # График для температуры точки росы (td2m - температура точки росы (град С))        
    
    fig_w_2 = plt.figure(figsize = (14,10))
    w_ax2 = fig_w_2.add_subplot(111)
    nam_4 = u'Плотность снега'
    nam_5 = u'Плотность снега, кг/м3'
    #l_p = 'upper left'
    #colo_1 = 'r'
    rho = plot_16(w_ax2, ts_rho_1, ts_rho_2, ts_rho_3, ts_rho_4, ts_rho_5, ts_rho_6, ts_rho_7, ts_rho_8, ts_rho_9, ts_rho_10, ts_rho_11, ts_rho_12, ts_rho_13, ts_rho_14, ts_rho_15, ts_rho_16, nam_4, nam_5, 0, 701, 100, minorLocator_2, y_w_1, y_w_2, 0, 751)
    plt.savefig(iPath_result + 'RHO_'+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
    #dew_point = plot_1(w_ax2,ts_rho, nam_1, nam_2, nam_3, 0, 701, 100, minorLocator_2, l_p, y_w_1, y_w_2, colo_1)
        
    # График для температуры точки росы (td2m - температура точки росы (град С))        
    fig_w_3 = plt.figure(figsize = (14,10))
    w_ax3 = fig_w_3.add_subplot(111)
    nam_6 = u'Запас воды в снеге'
    nam_7 = u'Запас воды в снеге, мм'
    #l_p = 'upper left'
    #colo_1 = 'b'
    swe = plot_16(w_ax3, ts_swe_1, ts_swe_2, ts_swe_3, ts_swe_4, ts_swe_5, ts_swe_6, ts_swe_7, ts_swe_8, ts_swe_9, ts_swe_10, ts_swe_11, ts_swe_12, ts_swe_13, ts_swe_14, ts_swe_15, ts_swe_16, nam_6, nam_7, 0, 251, 15, minorLocator_3, y_w_1, y_w_2, 0, 250)
    #dew_point = plot_1(w_ax3, ts_swe, nam_1, nam_2, nam_3, 0, 151, 15, minorLocator_3, l_p, y_w_1, y_w_2, colo_1)
            
    plt.savefig(iPath_result + 'SWE_'+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
    plt.gcf().clear()
    
