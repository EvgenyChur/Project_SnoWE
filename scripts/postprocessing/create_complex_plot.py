# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:43:40 2018

@author: Evgenii Churiulin
Скрипт meteo_kat_plot.py - Скрипт предназначен для отрисовки графиков на основе
метеорологических данных за два временных интервала: год и зимний сезон.
В текущей версии работа скрипта фокусируется на обработке данных с метеостанции
располагающихся в Москве и Московской области. Скрипт может быть переделан для
любого водосбора, путем изменения путей к исходным данным;
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

minorLocator_4 = AutoMinorLocator (n=2)
minorFormatter_4 = FormatStrFormatter('%.1f')

minorLocator_5 = AutoMinorLocator (n=2)
minorFormatter_5 = FormatStrFormatter('%.1f')

minorLocator_6 = AutoMinorLocator (n=2)
minorFormatter_6 = FormatStrFormatter('%.1f')

minorLocator_7 = AutoMinorLocator (n=2)
minorFormatter_7 = FormatStrFormatter('%.1f')

minorLocator_8 = AutoMinorLocator (n=2)
minorFormatter_8 = FormatStrFormatter('%.1f')

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
    ax.set_title(n_4, color = 'black', fontsize = 14)
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
    ax.plot(pr_1.index, pr_1, label = na_1, color = 'b', linestyle = '-')
    ax.plot(pr_2.index, pr_2, label = na_2, color = 'r', linestyle = '-')
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
    ax.set_title(nam_2, color = 'black', fontsize = 14)
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
    bx.set_title(nam_2, color = 'black', fontsize = 14)
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

#Версия для работы по одной станции
#fileName = '27515.csv'
#iPath = 'D:/Churyulin/msu_cosmo/Moscow_data/1_day/{}'.format(fileName)
#iPath = 'D:/Churyulin/msu_cosmo/Moscow_data/result_2000_2018/' #Москвоские метеорологические станции
iPath = 'D:/Churyulin/DV/result_1_month_2011_2019/'
dirs_csv = os.listdir(iPath)



#Путь к графикам за весь год
#iPath_2 = 'D:/Churyulin/msu_cosmo/Moscow_data/Plot_for_year/'
iPath_2 = 'D:/Churyulin/DV/plot/'
dirs_result_year = os.listdir(iPath_2)
for file in dirs_result_year:
    os.remove(iPath_2 + file)

#Путь к финальному результату (графики с фильтром для зимы)
#iPath_3 = 'D:/Churyulin/msu_cosmo/Moscow_data/Winter_plot/'
iPath_3 = 'D:/Churyulin/DV/result_plot_2011_2019/'
dirs_result_winter = os.listdir(iPath_3)
for file in dirs_result_winter:
    os.remove(iPath_3 + file)


for file in dirs_csv:
    try:
        fileName_csv = file
        iPath_csv = (iPath + fileName_csv)
        #Чтение csv и выкидка не нужных значенией
        df = pd.read_csv(iPath_csv, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                         skipinitialspace = True, na_values= ['9990','********'])
        print ('Columns:', df.columns)
        
        #Работа с формой для комплексного графика
        rcParams['figure.subplot.left'] = 0.1  # Левая граница
        rcParams['figure.subplot.right']= 0.95  # Правая граница
        rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
        rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
        rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots

        """
        s = 7
        periods = [['2011-10-01','2012-04-30'],
                   ['2012-10-01','2013-04-30'],
                   ['2013-10-01','2014-04-30'],
                   ['2014-10-01','2015-04-30'],
                   ['2015-10-01','2016-04-30'],
                   ['2016-10-01','2017-04-30'],
                   ['2017-10-01','2018-04-30']]
        
        periods = np.array(periods)
        print (periods)
        for k in range(s):
            y1 = periods[k][0]
            y2 = periods[k][1]
            ts_ps = df['ps'][y1:y2]
            ts_pmsl = df['pmsl'][y1:y2]
            ts_t2m = df['t2m'][y1:y2]
            ts_td2m = df['td2m'][y1:y2]
            ts_dd10m = df['dd10m'][y1:y2]
            ts_ff10m = df['ff10m'][y1:y2]
            ts_tmin2m = df['tMin2m'][y1:y2]
            ts_tmax2m = df['tMax2m'][y1:y2]
            ts_tming = df['tMinG'][y1:y2]
            ts_R12 = df['R12'][y1:y2]
            ts_R24 = df['R24'][y1:y2]
            ts_t_g = df['t_g'][y1:y2]
            ts_hsnow = df['hSnow'][y1:y2]
        
            type(df.index)
            #Работа с графиком
            #plt.style.use('ggplot')
            fig = plt.figure(figsize = (14,10))
            
            #Задание координатной сетки и места где будут располагаться графики
            egrid = (4,4)
            ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
            ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
            ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
            ax4 = plt.subplot2grid(egrid, (3,0), colspan = 4)
            
            # График для температура воздуха: t2m - температура воздуха (град С);
            #tmin2m - минимальная температура воздуха (град С)- tmax2m - максимальная температура воздуха (град С)    
            n_1 = 'max T'
            n_2 = 'avg T'
            n_3 = 'min T'
            n_4 =  u'Температура воздуха'
            n_5 = u'Температура, С'
            l_p = 'upper left'
            temperatura = plot_3(ax1, ts_tmax2m, ts_t2m, ts_tmin2m, n_1, n_2, n_3, n_4, n_5, -30, 31, 15, minorLocator_1, l_p, y1, y2)
            
            # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
            #t_g - температура поверхности почвы (град С)       
            na_1 = 'soil temp'
            na_2 = 'min soil temp'
            na_3 = u'Температуры поверхности почвы'
            na_4 = u'Температура, С'
            l_p = 'upper left'
            soil_temp = plot_2(ax2, ts_t_g, ts_tming, na_1, na_2, na_3, na_4, -30, 31, 15, minorLocator_2, l_p, y1, y2)
            
            # График для температуры точки росы (td2m - температура точки росы (град С))        
            nam_1 = 'dew point'
            nam_2 = u'Температура точки росы'
            nam_3 = u'Температура, С'
            l_p = 'upper left'
            colo_1 = 'r'
            dew_point = plot_1(ax3,ts_td2m, nam_1, nam_2, nam_3, -30, 31, 15, minorLocator_3, l_p, y1, y2, colo_1)
            
            # График для давления: ps - давление на уровне станции (гПа); pmsl - давление, приведенное к уровню моря (гПа)
            name_1 = 'air ps station level'
            name_2 = 'air ps sea level'
            name_3 = u'Атмосферное давление'
            name_4 = u'Атм-ое давление, гПа'
            l_po = 'lower left'
            air_pressure = plot_2(ax4, ts_ps, ts_pmsl, name_1, name_2, name_3, name_4, 940, 1041, 20, minorLocator_4, l_po, y1, y2)
            
            plt.savefig(iPath_2 + 'Complex schedule_1_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y1,y2), format='png', dpi = 300)
            #plt.savefig(iPath_2 + fileName[0:5] +'.png', format='png', dpi = 300)
            #plt.show()
            plt.gcf().clear()
            
            #Работа с графиком
            #plt.style.use('ggplot')
            fig2 = plt.figure(figsize = (14,10))
                
            #Задание координатной сетки и места где будут располагаться графики
            egrid_2 = (3,4)
            bx1 = plt.subplot2grid(egrid_2, (0,0), colspan = 4)
            bx2 = plt.subplot2grid(egrid_2, (1,0), colspan = 4)
            bx3 = plt.subplot2grid(egrid_2, (2,0), colspan = 4)
            
            # График для осадков за 12 час, мм - RAINS 
            name_01 = 'precip 12 hour'
            name_02 = u'Осадки за 12 часов'
            name_03 = u'Осадки, мм'
            l_p = 'upper left'
            col = 'g'
            precipitation_12 = bar_char_1(bx1, ts_R12, name_01, name_02, name_03, 0, 31, 10, minorLocator_5, l_p, col, y1, y2)
            
            #График для осадков за 24 часа, мм - RAINS
            name_001 = 'precip 24 hour'
            name_002 = u'Осадки за 24 часа'
            name_003 = u'Осадки, мм'
            l_p = 'upper left'
            col = 'g'
            precipitation_24 = bar_char_1(bx2, ts_R24, name_001, name_002, name_003, 0, 71, 10, minorLocator_6, l_p, col, y1, y2)
            
            #График для высоты снежного покрова, см
            name_0001 = 'snow'
            name_0002 = u'Высота снежного покрова'
            name_0003 = u'Высота снега, см'
            l_p = 'upper left'
            colo = 'b'
            snow_24 = bar_char_1(bx3, ts_hsnow, name_0001, name_0002, name_0003, 0, 61, 20, minorLocator_7, l_p, colo, y1, y2)
            
            plt.savefig(iPath_2 + 'Complex schedule_2_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y1,y2), format='png', dpi = 300)
            plt.gcf().clear()    
            
            
            fig3 = plt.figure(figsize = (14,10))
            
            #Задание координатной сетки и места где будут располагаться графики
            egrid_3 = (2,4)
            cx1 = plt.subplot2grid(egrid_3, (0,0), colspan = 4)
            cx2 = plt.subplot2grid(egrid_3, (1,0), colspan = 4)
            
            # График для ff10m - скорость ветра (м/сек) на высоте 10 метров
            nam_01 = 'U wind'
            nam_02 = u'Скорость ветра'
            nam_03 = u'Скорость ветра, м/с'
            l_p = 'upper left'
            colo = 'm'
            wind = plot_1(cx1,ts_ff10m, nam_01, nam_02, nam_03, 0, 7, 2, minorLocator_8, l_p, y1, y2, colo)                                    
                
            # График для dd10m - направления ветра (град) на высоте 10 метров
            name_00001 = 'wind direction'
            name_00002 = u'Направление ветра'
            name_00003 = u'Направление ветра, град'
            l_p = 'upper left'
            colo_1 = 'm'
            wind_direction = bar_char_1(cx2, ts_dd10m, name_00001, name_00002, name_00003, 0, 361, 72, minorLocator_9, l_p, colo_1, y1, y2)
                
            plt.savefig(iPath_2 + 'Complex schedule_3_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y1,y2), format='png', dpi = 300)
            plt.gcf().clear()
        """
    
        """
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
        """
        """
        w = 7  
        periods_winter = [['2011-10-01','2012-04-30'],
                          ['2012-10-01','2013-04-30'],
                          ['2013-10-01','2014-04-30'],
                          ['2014-10-01','2015-04-30'],
                          ['2015-10-01','2016-04-30'],
                          ['2016-10-01','2017-04-30'],
                          ['2017-10-01','2018-04-30']]
        """
        w = 7  
        periods_winter = [['2011-01-01','2011-12-31'],
                          ['2012-01-01','2013-12-31'],
                          ['2013-01-01','2014-12-31'],
                          ['2014-01-01','2015-12-31'],
                          ['2015-01-01','2016-12-31'],
                          ['2016-01-01','2017-12-31'],
                          ['2017-01-01','2018-12-31']]
        periods_winter = np.array(periods_winter)
        print (periods_winter)
        for tr in range(w):
            y_w_1 = periods_winter[tr][0]
            y_w_2 = periods_winter[tr][1]
            ts_ps_w = df['ps'][y_w_1:y_w_2]
            ts_pmsl_w = df['pmsl'][y_w_1:y_w_2]
            ts_t2m_w = df['t2m'][y_w_1:y_w_2]
            ts_td2m_w = df['td2m'][y_w_1:y_w_2]
            ts_dd10m_w = df['dd10m'][y_w_1:y_w_2]
            ts_ff10mean_w = df['ff10meanm'][y_w_1:y_w_2] #внимание
            ts_ff10max_w = df['ff10max'][y_w_1:y_w_2]
            ts_tmin2m_w = df['tMin2m'][y_w_1:y_w_2]
            ts_tmax2m_w = df['tMax2m'][y_w_1:y_w_2]
            ts_tming_w = df['tMinG'][y_w_1:y_w_2]
            ts_R12_w = df['R12'][y_w_1:y_w_2]
            ts_R24_w = df['R24'][y_w_1:y_w_2]
            ts_t_g_w = df['t_g'][y_w_1:y_w_2]
            ts_hsnow_w = df['hSnow'][y_w_1:y_w_2]
            
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
            #tmin2m - минимальная температура воздуха (град С)- tmax2m - максимальная температура воздуха (град С)    
            n_1 = 'max T'
            n_2 = 'avg T'
            n_3 = 'min T'
            n_4 =  u'Температура воздуха'
            n_5 = u'Температура, С'
            l_p = 'upper left'
            temperatura = plot_3(w_ax1, ts_tmax2m_w, ts_t2m_w, ts_tmin2m_w, n_1, n_2, n_3, n_4, n_5, -30, 31, 15, minorLocator_1, l_p, y_w_1, y_w_2)
            
            # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
            #t_g - температура поверхности почвы (град С)       
            na_1 = 'soil temp'
            na_2 = 'min soil temp'
            na_3 = u'Температуры поверхности почвы'
            na_4 = u'Температура, С'
            l_p = 'upper left'
            soil_temp = plot_2(w_ax2, ts_t_g_w, ts_tming_w, na_1, na_2, na_3, na_4, -30, 31, 15, minorLocator_2, l_p, y_w_1, y_w_2)
        
            # График для температуры точки росы (td2m - температура точки росы (град С))        
            nam_1 = 'dew point'
            nam_2 = u'Температура точки росы'
            nam_3 = u'Температура, С'
            l_p = 'upper left'
            colo_1 = 'r'
            dew_point = plot_1(w_ax3,ts_td2m_w, nam_1, nam_2, nam_3, -30, 31, 15, minorLocator_3, l_p, y_w_1, y_w_2, colo_1)
            
            # График для давления: ps - давление на уровне станции (гПа); pmsl - давление, приведенное к уровню моря (гПа)
            name_1 = 'air ps station level'
            name_2 = 'air ps sea level'
            name_3 = u'Атмосферное давление'
            name_4 = u'Атм-ое давление, гПа'
            l_po = 'lower left'
            air_pressure = plot_2(w_ax4, ts_ps_w, ts_pmsl_w, name_1, name_2, name_3, name_4, 940, 1041, 20, minorLocator_4, l_po, y_w_1, y_w_2)
            
            plt.savefig(iPath_3 + 'Complex schedule_1_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
            #plt.savefig(iPath_2 + fileName[0:5] +'.png', format='png', dpi = 300)
            plt.gcf().clear()
            
            #Работа с графиком
            #plt.style.use('ggplot')
            fig_w_2 = plt.figure(figsize = (14,10))
                
            #Задание координатной сетки и места где будут располагаться графики
            egrid_w_2 = (3,4)
            w_bx1 = plt.subplot2grid(egrid_w_2, (0,0), colspan = 4)
            w_bx2 = plt.subplot2grid(egrid_w_2, (1,0), colspan = 4)
            w_bx3 = plt.subplot2grid(egrid_w_2, (2,0), colspan = 4)
            
            # График для осадков за 12 час, мм - RAINS 
            name_01 = 'precip 12 hour'
            name_02 = u'Осадки за 12 часов'
            name_03 = u'Осадки, мм'
            l_p = 'upper left'
            col = 'g'
            precipitation_12 = bar_char_1(w_bx1, ts_R12_w, name_01, name_02, name_03, 0, 31, 10, minorLocator_5, l_p, col, y_w_1, y_w_2)
            
            #График для осадков за 24 часа, мм - RAINS
            name_001 = 'precip 24 hour'
            name_002 = u'Осадки за 24 часа'
            name_003 = u'Осадки, мм'
            l_p = 'upper left'
            col = 'g'
            precipitation_24 = bar_char_1(w_bx2, ts_R24_w, name_001, name_002, name_003, 0, 71, 10, minorLocator_6, l_p, col, y_w_1, y_w_2)
            
            #График для высоты снежного покрова, см
            name_0001 = 'snow'
            name_0002 = u'Высота снежного покрова'
            name_0003 = u'Высота снега, см'
            l_p = 'upper left'
            colo = 'b'
            snow_24 = bar_char_1(w_bx3, ts_hsnow_w, name_0001, name_0002, name_0003, 0, 61, 20, minorLocator_7, l_p, colo, y_w_1, y_w_2)
            
            plt.savefig(iPath_3 + 'Complex schedule_2_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
            plt.gcf().clear()    
            
            
            fig_w_3 = plt.figure(figsize = (14,10))
        
            #Задание координатной сетки и места где будут располагаться графики
            egrid_w_3 = (2,4)
            w_cx1 = plt.subplot2grid(egrid_w_3, (0,0), colspan = 4)
            w_cx2 = plt.subplot2grid(egrid_w_3, (1,0), colspan = 4)
            
            # График для ff10m - скорость ветра (м/сек) на высоте 10 метров
            nam_01 = 'U wind'
            nam_02 = u'Скорость ветра'
            nam_03 = u'Скорость ветра, м/с'
            l_p = 'upper left'
            colo = 'm'
            wind = plot_1(w_cx1,ts_ff10m_w, nam_01, nam_02, nam_03, 0, 7, 2, minorLocator_8, l_p, y_w_1, y_w_2, colo)                                    
            
            # График для dd10m - направления ветра (град) на высоте 10 метров
            name_00001 = 'wind direction'
            name_00002 = u'Направление ветра'
            name_00003 = u'Направление ветра, град'
            l_p = 'upper left'
            colo_1 = 'm'
            wind_direction = bar_char_1(w_cx2, ts_dd10m_w, name_00001, name_00002, name_00003, 0, 361, 72, minorLocator_9, l_p, colo_1, y_w_1, y_w_2)
        
            plt.savefig(iPath_3 + 'Complex schedule_3_'+fileName_csv[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
            plt.gcf().clear()

                
    except NameError as error:
        print ( 'Exception: ', error )
