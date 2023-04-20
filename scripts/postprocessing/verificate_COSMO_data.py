# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 17:01:16 2018

@author: Churiulin E.V

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter
from matplotlib import rcParams
import os

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
#def plot_2(ax, pr_1, pr_2, na_1, na_2, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p):
def plot_3(ax, pr_1, pr_2, prr_3, na_1, na_2, nan_3, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p):

    ax.plot(pr_1.index, pr_1, label = na_1, color = 'tab:blue', linestyle = '-', alpha = 0.5)
    ax.plot(pr_2.index, pr_2, label = na_2, color = 'tab:orange', linestyle = '-.')
    ax.plot(prr_3.index, prr_3, label = nan_3, color = 'tab:green', linestyle = '-.')
    
    ax.set_title(na_3, color = 'black', fontsize = 16)
    #ax2.text('2016-10-10', 20.0, 'II', fontsize = 20, color= 'c')
    ax.set_ylabel(na_4, color = 'black', fontsize = 16)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on')
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim('2018-09-01','2019-05-31')
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(16)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    


#Версия для работы по одной станции КОСМО
#fileName = 'data_22559.csv' # Name of the meteorological station - model version
#iPath_1 = 'D:/Churyulin/msu_cosmo/forecast/presipitation/final_result_station/0 - 24/{}'.format(fileName)
iPath_1 = 'D:/Churyulin/DVINA/result_general/data_series/original_COSMO/0-24/'
iPath_3 = 'D:/Churyulin/DVINA/result_general/data_series/Hybrid/0-24/'

dirs_forec = sorted(os.listdir(iPath_1))
dirs_forec = sorted(os.listdir(iPath_3))

#Версия для работы по одной станции РЕАЛ
#fileName_1 = '22559.csv' # Name of the meteorological station - model version
#iPath_2 = 'D:/Churyulin/msu_cosmo/real_meteo/1_day/{}'.format(fileName_1)

iPath_2 = 'D:/Churyulin/DVINA/meteo/result_2000_2019/'
dirs_real = sorted(os.listdir(iPath_2))

#Загрузка и очистка папки с результатими 
out_path = 'D:/Churyulin/DVINA/result_general/verification_plot/'
dirs_out = os.listdir(out_path)
for file in dirs_out:
    os.remove(out_path + file)
    
"""    
#Функция для считывания данных из файлов
for i in dirs_forec:
    fileName_forec = i
    iPath_forec = (iPath_1 + fileName_forec)
    
    df_cosmo = pd.read_csv(iPath_1, sep = ',', header = 0)
    
    times = pd.date_range('2018-01-01', '2018-08-05', freq ='1d' )

    t_2m = pd.Series(df_cosmo['T_2M'].values, index=times, name = 'T_2M')
    td_2m = pd.Series(df_cosmo['TD_2M'].values, index=times, name = 'TD_2M')
    relhum_2m = pd.Series(df_cosmo['RELHUM_2M'].values, index=times, name = 'RELHUM_2M')
    qv_s = pd.Series(df_cosmo['QV_S'].values, index=times, name = 'QV_S')
    tot_precip = pd.Series(df_cosmo['TOT_PREC'].values, index=times, name = 'TOT_PREC')

    t_2m = t_2m - 273
    td_2m = td_2m - 273
    
    
for j in dirs_real:
    fileName_real = j
    iPath_real = (iPath_2 + fileName_real)
"""    

try:
    for i in dirs_real:
        fileName_real = i
        fileName_test = 'data_'+ i
        
        print (fileName_test)
        
        iPath_real = (iPath_2 + fileName_real)
        iPath_cosmo = (iPath_1 + fileName_test)
        iPath_hybrid = (iPath_3 + fileName_test)
        
        df_real = pd.read_csv(iPath_real, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                              skipinitialspace = True, na_values= ['9990','********'])
        
        df_real = df_real[np.isfinite(df_real['R24'])]
        R24 = df_real.iloc[:,15]
            #Коррекция данных по сумме осадков за 24 часа
        for i, xi in enumerate(R24):
            if xi > 50:
                R24[i] = 0
            elif xi < 0:
                R24[i] = 0              
            
            elif (R24[i]-R24[i-1]) > 40:
                R24[i] = (R24[i+1]+R24[i-1])/2
            
        
        
        df_cosmo = pd.read_csv(iPath_cosmo, sep = ',', header = 0)
        
        
        year = df_cosmo.iloc[:,0]
        month = df_cosmo.iloc[:,1]
        day = df_cosmo.iloc[:,2]
        meteo_dates = [pd.to_datetime('{}-{}-{}'.format(i, j, z), format='%Y-%m-%d') for i,j,z, in zip(year, month,day)] 
        
        
        #times = pd.date_range('2018-01-01', '2018-08-05', freq ='1d' )
        
        t_2m = pd.Series(df_cosmo['T_2M'].values, index=meteo_dates, name = 'T_2M')
        td_2m = pd.Series(df_cosmo['TD_2M'].values, index=meteo_dates, name = 'TD_2M')
        relhum_2m = pd.Series(df_cosmo['RELHUM_2M'].values, index=meteo_dates, name = 'RELHUM_2M')
        qv_s = pd.Series(df_cosmo['QV_S'].values, index=meteo_dates, name = 'QV_S')
        tot_precip = pd.Series(df_cosmo['TOT_PREC'].values, index=meteo_dates, name = 'TOT_PREC')
        
        
        
        df_hybrid = pd.read_csv(iPath_hybrid, sep = ',', header = 0)
        
        year_h = df_hybrid.iloc[:,0]
        month_h = df_hybrid.iloc[:,1]
        day_h = df_hybrid.iloc[:,2]
        meteo_dates_h = [pd.to_datetime('{}-{}-{}'.format(a, b, c), format='%Y-%m-%d') for a,b,c, in zip(year_h, month_h,day_h)] 
        
        
        #times = pd.date_range('2018-01-01', '2018-08-05', freq ='1d' )
        
        t_2m_h = pd.Series(df_hybrid['T_2M'].values, index=meteo_dates_h, name = 'T_2M')
        td_2m_h = pd.Series(df_hybrid['TD_2M'].values, index=meteo_dates_h, name = 'TD_2M')
        relhum_2m_h = pd.Series(df_hybrid['RELHUM_2M'].values, index=meteo_dates_h, name = 'RELHUM_2M')
        qv_s_h = pd.Series(df_hybrid['QV_S'].values, index=meteo_dates_h, name = 'QV_S')
        tot_precip_h = pd.Series(df_hybrid['TOT_PREC'].values, index=meteo_dates_h, name = 'TOT_PREC')
        
        
        
        
        
        #Работа с формой для комплексного графика
        rcParams['figure.subplot.left'] = 0.1  # Левая граница
        rcParams['figure.subplot.right']= 0.95  # Правая граница
        rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
        rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
        rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots
        
        #Работа с графиком
        #plt.style.use('ggplot')
        fig = plt.figure(figsize = (14,10))
                
        #Задание координатной сетки и места где будут располагаться графики
        egrid = (3,4)
        ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
        ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
        ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
        
               
        
        # График для температуры воздуха (град С)
               
        na_1 = '1' #cosmo
        na_2 = '2' #in situ
        nan_3 = '3' # hybrid
        na_3 = 'I' #air temperature
        na_4 = u'Температура, С'
        l_p = 'lower left'
        #air_temp = plot_2(ax1, t_2m, df_real['t2m'], na_1, na_2, na_3, na_4, -30, 31, 15, minorLocator_1, l_p)
        air_temp = plot_3(ax1, t_2m, df_real['t2m'],t_2m_h, na_1, na_2, nan_3, na_3, na_4, -30, 31, 15, minorLocator_1, l_p)
        #air_temp = plot_2(ax1, t_2m, df_real['t2m'], na_1, na_2, na_3, na_4, minorLocator_1, l_p)
        
        # График для температуры точки росы (град С)
               
        na_1 = '1'
        na_2 = '2'
        nan_3 = '3'
        na_3 = 'II' #dew point
        na_4 = u'Температура, С'
        l_p = 'lower left'
        #td_temp = plot_2(ax2, td_2m, df_real['td2m'], na_1, na_2, na_3, na_4, -30, 31, 15, minorLocator_2, l_p)
        td_temp = plot_3(ax2, td_2m, df_real['td2m'],td_2m_h, na_1, na_2, nan_3, na_3, na_4, -30, 31, 15, minorLocator_2, l_p)
        
        #td_temp = plot_2(ax2, td_2m, df_real['td2m'], na_1, na_2, na_3, na_4, minorLocator_2, l_p)
        
        # График для осадков (мм)
               
        na_1 = '1'
        na_2 = '2'
        nan_3 = '3'
        na_3 = 'III' #precipitation
        na_4 = u'Осадки, мм'
        l_p = 'upper left'
        #prec = plot_2(ax3, tot_precip, df_real['R24'], na_1, na_2, na_3, na_4, 0, 31, 5, minorLocator_3, l_p)
        prec = plot_3(ax3, tot_precip, df_real['R24'], tot_precip_h, na_1, na_2, nan_3, na_3, na_4, 0, 31, 5, minorLocator_3, l_p)
        #prec = plot_2(ax3, tot_precip, df_real['R24'], na_1, na_2, na_3, na_4, minorLocator_3, l_p)
        
                
        plt.savefig(out_path + fileName_real[0:5] +'.png', format='png', dpi = 300)
        plt.gcf().clear()
        
except NameError as error:
    print ('Exception: ', error)
