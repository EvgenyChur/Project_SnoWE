# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 13:04:17 2018

@author: Evgeny Churiulin
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter

minorLocator_1 = AutoMinorLocator (n=1)
minorFormatter_1 = FormatStrFormatter('%.1f')

minorLocator_2 = AutoMinorLocator (n=1)
minorFormatter_2 = FormatStrFormatter('%.1f')

minorLocator_3 = AutoMinorLocator (n=1)
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
#def plot_2(ax, pr_1, pr_2, na_1, na_2, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):
def plot_2(ax, pr_1, pr_2, na_1, na_2, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p):    
    #ax.scatter(pr_1.index, pr_1, label = na_1, color = 'b', linestyle = '-')
    #ax.scatter(pr_2.index, pr_2, label = na_2, color = 'r', linestyle = '-')
    ax.plot(pr_1.index, pr_1, label = na_1, color = 'b',linewidth = 2.0)
    ax.scatter(pr_2.index, pr_2, s = 50, label = na_2, color = 'r')
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
    ax.set_xticks(pd.date_range('2011-09-01', '2012-04-30', freq = '1M'))
    #ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(16)
    yax.set_minor_locator(pr_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
"""
#meteo_file = 'stations_ivan.csv'
fileName_2 = 'field.csv'
iPath_2 = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison/result_filter/{}'.format(fileName_2)

result_exit = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison/in-situ/'

# Считываем базовые данные для работы с массивом метеорологических данных (снег)
df = pd.read_csv(iPath_2, sep = ';')
df = df.drop_duplicates()
df = df.set_index(['id_st'])


df_real = pd.read_csv(iPath_2, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                      skipinitialspace = True, na_values= ['9990','********'])

stations = df_real.iloc[:,0]
stations = stations.sort_values()
stations = stations.drop_duplicates()
for i in stations:
    id_station = i
    df_station = df.filter(like = str(id_station), axis = 0)
    df_station = df_station.reset_index()
    
    id_st = df_station.iloc[:,0]
    date = df_station.iloc[:,1]
    date = pd.to_datetime(date)
    
    route = df_station.iloc[:,2]
    sd = df_station.iloc[:,3]
    rho = df_station.iloc[:,4]
    swe = df_station.iloc[:,5]
            
    date.index = id_st.index = route.index = sd.index = rho.index = swe.index
    data_result = pd.concat([date, id_st, route, sd, rho, swe], axis = 1)
    #print ('Columns:', data_result_1.columns)
    data_result.columns = ['date','id_st','route','sd','rho','swe']
    data_result = data_result.set_index(['date'])
            
    data_result.to_csv(result_exit + str(i) +'.csv', sep=';', float_format='%.3f', index_label = 'date')
"""
fileName_station = '27417.csv'
iPath_snowe = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison/data_snowe/{}'.format(fileName_station)

iPath_in_situ = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison/in-situ/{}'.format(fileName_station)


iPath_3 = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison/'

df_snowe = pd.read_csv(iPath_snowe, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                       skipinitialspace = True, na_values= ['9990','********'])


df_27417 = pd.read_csv(iPath_in_situ, skiprows = 0, sep=';', dayfirst = True, parse_dates = True, index_col = [0],
                       skipinitialspace = True, na_values= ['9990','********'])

ts_sd_1_table = df_snowe['depth'] #Фактические сведения
ts_sd_2_table = df_27417['sd'] #модельные сведения
#ts_sd_1_table = ts_sd_1_table.drop_duplicates(keep = False)
#ts_sd_2_table = ts_sd_2_table.drop_duplicates()
df_sd = pd.concat([ts_sd_1_table, ts_sd_2_table], axis = 1, join='inner')
df_sd.to_csv(iPath_3 +'sd_' + fileName_station[0:5] +'.csv', sep=';', float_format='%.3f',
             header = ['in situ','model'], index_label = 'Index')


ts_rho_1_table = df_snowe['rho'] #Фактические сведения
ts_rho_2_table = df_27417['rho'] #модельные сведения   
df_rho = pd.concat([ts_rho_1_table/1000, ts_rho_2_table], axis = 1, join='inner')   
df_rho.to_csv(iPath_3 + 'rho_' + fileName_station[0:5] +'.csv', sep=';', float_format='%.3f',
              header = ['in situ','model'], index_label = 'Index')

ts_swe_1_table = df_snowe['swe'] #Фактические сведения
ts_swe_2_table = df_27417['swe'] #модельные сведения
df_swe = pd.concat([ts_swe_1_table, ts_swe_2_table], axis = 1, join='inner')  
df_swe.to_csv(iPath_3 + 'swe_' + fileName_station[0:5] +'.csv', sep=';', float_format='%.3f',
              header = ['in situ','model'], index_label = 'Index') 

#Работа с формой для комплексного графика
rcParams['figure.subplot.left'] = 0.1  # Левая граница
rcParams['figure.subplot.right']= 0.95  # Правая граница
rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots

#Для станции 27515 нету данных за 2006 и 2007 год
#Для станции 27627 нету данных за 2006 - 2008 год
#w = 12 
""" 
w = 12
periods_winter = [['2006-09-01','2007-04-30'],
                  ['2007-09-01','2008-04-30'],
                  ['2008-09-01','2009-04-30'],
                  ['2009-09-01','2010-04-30'],
                  ['2010-09-01','2011-04-30'],
                  ['2011-09-01','2012-04-30'],
                  ['2012-09-01','2013-04-30'],
                  ['2013-09-01','2014-04-30'],
                  ['2014-09-01','2015-04-30'],
                  ['2015-09-01','2016-04-30'],
                  ['2016-09-01','2017-04-30'],
                  ['2017-09-01','2018-04-30']]
"""
w = 46
periods_winter = [['2011-09-01','2011-09-10'],
                  ['2011-09-01','2011-09-15'],
                  ['2011-09-01','2011-09-20'],
                  ['2011-09-01','2011-09-25'],
                  ['2011-09-01','2011-09-30'],
                  ['2011-09-01','2011-10-05'],
                  ['2011-09-01','2011-10-10'],
                  ['2011-09-01','2011-10-15'],
                  ['2011-09-01','2011-10-20'],
                  ['2011-09-01','2011-10-25'],
                  ['2011-09-01','2011-10-30'],
                  ['2011-09-01','2011-11-05'],
                  ['2011-09-01','2011-11-10'],
                  ['2011-09-01','2011-11-15'],
                  ['2011-09-01','2011-11-20'],
                  ['2011-09-01','2011-11-25'],
                  ['2011-09-01','2011-11-30'],
                  ['2011-09-01','2011-12-05'],
                  ['2011-09-01','2011-12-10'],
                  ['2011-09-01','2011-12-15'],
                  ['2011-09-01','2011-12-20'],
                  ['2011-09-01','2011-12-25'],
                  ['2011-09-01','2011-12-30'],
                  ['2011-09-01','2012-01-05'],
                  ['2011-09-01','2012-01-10'],
                  ['2011-09-01','2012-01-15'],
                  ['2011-09-01','2012-01-20'],
                  ['2011-09-01','2012-01-25'],
                  ['2011-09-01','2012-01-30'],
                  ['2011-09-01','2012-02-05'],
                  ['2011-09-01','2012-02-10'],
                  ['2011-09-01','2012-02-15'],
                  ['2011-09-01','2012-02-20'],
                  ['2011-09-01','2012-02-25'],
                  ['2011-09-01','2012-03-05'],
                  ['2011-09-01','2012-03-10'],
                  ['2011-09-01','2012-03-15'],
                  ['2011-09-01','2012-03-20'],
                  ['2011-09-01','2012-03-25'],
                  ['2011-09-01','2012-03-30'],
                  ['2011-09-01','2012-04-05'],
                  ['2011-09-01','2012-04-10'],
                  ['2011-09-01','2012-04-15'],
                  ['2011-09-01','2012-04-20'],
                  ['2011-09-01','2012-04-25'],
                  ['2011-09-01','2012-04-30'],]
                                  
        
periods_winter = np.array(periods_winter)
#print (periods_winter)
for tr in range(w):
    y_w_1 = periods_winter[tr][0]
    print (y_w_1)
    y_w_2 = periods_winter[tr][1]
    print (y_w_2)
    ts_sd_1 = df_snowe['depth'][y_w_1:y_w_2] #Фактические сведения
    ts_sd_2 = df_27417['sd'][y_w_1:y_w_2] #модельные сведения
      
    ts_rho_1 = df_snowe['rho'][y_w_1:y_w_2] #Фактические сведения
    ts_rho_2 = df_27417['rho'][y_w_1:y_w_2] #модельные сведения
    
    ts_swe_1 = df_snowe['swe'][y_w_1:y_w_2] #Фактические сведения
    ts_swe_2 = df_27417['swe'][y_w_1:y_w_2] #модельные сведения

    fig = plt.figure(figsize = (14,10))
    #Задание координатной сетки и места где будут располагаться графики
    egrid = (3,4)
    ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
    ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
    ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
    # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
    #t_g - температура поверхности почвы (град С)       
    na_1 = u'Model'
    na_2 = u'in-situ'
    na_3 = u'Snow depth'
    na_4 = u'Snow depth, sm'
    l_p = 'upper left'
    #snow_sd = plot_2(ax1, ts_sd_1, ts_sd_2, na_1, na_2, na_3, na_4, 0, 61, 15, minorLocator_1, l_p, y_w_1, y_w_2)
    snow_sd = plot_2(ax1, ts_sd_1, ts_sd_2, na_1, na_2, na_3, na_4, 0, 61, 15, minorLocator_1, l_p)
    
    # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
    #t_g - температура поверхности почвы (град С)       
    na_1 = 'Model'
    na_2 = 'in-situ'
    na_3 = u'Snow density'
    na_4 = u'Snow density, g/sm3'
    l_p = 'upper left'
    #snow_rho = plot_2(ax2, ts_rho_1/1000, ts_rho_2, na_1, na_2, na_3, na_4, 0, 1, 0.25, minorLocator_2, l_p, y_w_1, y_w_2)
    snow_rho = plot_2(ax2, ts_rho_1/1000, ts_rho_2, na_1, na_2, na_3, na_4, 0, 1, 0.25, minorLocator_2, l_p)  
    # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
    #t_g - температура поверхности почвы (град С)       
    na_1 = u'Model'
    na_2 = u'in-situ'
    na_3 = u'Snow water equivalent'
    na_4 = u'Snow water equivalent, mm'
    l_p = 'upper left'
    #snow_swe = plot_2(ax3, ts_swe_1, ts_swe_2, na_1, na_2, na_3, na_4, 0, 151, 15, minorLocator_3, l_p, y_w_1, y_w_2)
    snow_swe = plot_2(ax3, ts_swe_1, ts_swe_2, na_1, na_2, na_3, na_4, 0, 151, 15, minorLocator_3, l_p)
    plt.savefig(iPath_3 + 'plot_' + fileName_station[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
    plt.gcf().clear()

"""
    fig = plt.figure(figsize = (14,10))
    #Задание координатной сетки и места где будут располагаться графики
    egrid = (3,4)
    ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
    ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
    ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
    

    ax1.plot(ts_sd_1.index, ts_sd_1, color = 'blue', linestyle = '-')
    ax1.scatter(ts_sd_2.index, ts_sd_2, color = 'red')
    
    ax2.plot(ts_swe_1.index, ts_swe_1, color = 'green', linestyle = '-')
    ax2.scatter(ts_swe_2.index, ts_swe_2, color = 'red')
    
    ax3.plot(ts_rho_1.index, ts_rho_1, color = 'black', linestyle = '-')
    ax3.scatter(ts_rho_2.index, ts_rho_2*1000, color = 'green')
    
    #ax4.plot(data_result.index, data_result['PRESS'], color = 'blue', linestyle = '-')

    #plt.savefig(iPath_3 + 'plot_1' +'.png', format='png', dpi = 300)
    plt.savefig(iPath_3 + 'plot_' + fileName_station[0:5] +' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300) 
    plt.gcf().clear()
"""
    
