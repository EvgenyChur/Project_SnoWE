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


from matplotlib import rcParams

import lib4processing as l4p
import lib4system_suport as l4s
import lib4time_periods as l4tp


lpreprocessing = True
lmain_calc = True
ltime_decade = True
lcompex = 1 # 2

# -- Users time period settings:
# --          Option 1      Option 2      Option 3      Option 4
ref_date1 = '2000-10-01' # '2018-09-01' #'2011-01-01' # 2011
ref_date2 = '2001-05-31' # '2019-05-31' #'2011-12-31' # 2019
n_periods = 19           #     1             7        #
years2add = 1            #     1             1        # 1

# -- Months
months = ['09', '10', '11', '12', '01', '02', '03', '04', '05']


def plot_3(ax,pr_1,pr_2,pr_3,n_1, n_2, n_3, n_4, n_5, pr_6, pr_7, pr_8, pr_9, l_p, time_step_1, time_step_2):
    ax.plot(pr_1.index, pr_1, label = n_1, color = 'r', linestyle = '-')
    ax.plot(pr_2.index, pr_2, label = n_2, color = 'm', linestyle = '-')
    ax.plot(pr_3.index, pr_3, label = n_3, color = 'b',  linestyle = '-' )

def plot_2(ax, pr_1, pr_2, na_1, na_2, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2):
    ax.plot(pr_1.index, pr_1, label = na_1, color = 'r', linestyle = '-')
    ax.plot(pr_2.index, pr_2, label = na_2, color = 'b', linestyle = '-')
    
def plot_1(ax, pr_1, nam_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, time_step_1, time_step_2, c):
    ax.plot(pr_1.index, pr_1, label = nam_1, color = c, linestyle = '-')

def bar_char_1(bx, pr_1, nam_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, c, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = c)

def bar_char_prec_1(bx, pr_1, prr_2, nam_1, nam_2, nam_3, nam_4, pr_2, pr_3, pr_4, pr_5, l_p, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = 'tab:blue') #твердые осадки
    bx.bar(prr_2.index, prr_2, label = nam_2, color = 'tab:green') #жидкие осадки

def plot_3_snow(ax, prr_1, prr_2, prr_3, name_1, name_2, name_3, na_3, na_4, pr_3, pr_4, pr_5, pr_6, l_p, time_step_1, time_step_2): # для отрисовки гибрида
    ax.plot(prr_1.index, prr_1, label = name_1, color = 'tab:blue', linestyle = '-') #Для SnoWE
    ax.scatter(prr_2.index, prr_2, label = name_2, color = 'tab:red', marker = '^') #Для полевых снегомерных маршрутов
    ax.scatter(prr_3.index, prr_3, label = name_3, color = 'tab:purple', marker = 'o') #Для лесных снегомерных маршрутов

def bar_char_2(bx, pr_1, prr_1, nam_1, name_1, nam_2, nam_3, pr_2, pr_3, pr_4, pr_5, l_p, c, time_step_1, time_step_2):
    bx.bar(pr_1.index, pr_1, label = nam_1, color = c)
    bx.plot(prr_1.index, prr_1, label = name_1, color = 'tab:red', linestyle = '-', linewidth = 2.5)
    

if lpreprocessing is True:
    # Preprocessing of snow survey data:
    main = 'D:/Churyulin/DON'
    
    # Input paths (field and forest survey):
    pin_field  = main + '/result_filter/field.csv'
    pin_forest = main + '/result_filter/forest.csv'
    
    # Output paths (field and forest survey):
    pou_field  = main + '/snow_survey/field/'
    pou_forest = main + '/snow_survey/forest/'

    # Cleaning previous results:
    l4s.clean_history(pou_field)
    l4s.clean_history(pou_forest)

    # Load and preprocessing of field and forest snow survey
    df_route_field  = l4p.get_obs_data(pin_field , pou_field)
    df_route_forest = l4p.get_obs_data(pin_forest, pou_forest)

if lmain_calc is True:
    # Input paths:
    #iPath = 'D:/Churyulin/DON/meteo_in_situ_data_2000_2019/' # путь к данным метеорологических наблюдений SYNOP
    iPath = 'D:/Churyulin/DON/test/'
    iPath_field = 'D:/Churyulin/DON/snow_survey/field/' # Путь к данным для метеостанции (полевой маршрут)
    iPath_forest = 'D:/Churyulin/DON/snow_survey/forest/' #Путь к данных для метеостанции (лесной маршрут)
    #iPath_snowe = 'D:/Churyulin/DON/snowe_data/'
    iPath_snowe = 'D:/Churyulin/DON/test_snowe/'


    # Output paths:
    iPath_max_snow = 'D:/Churyulin/DON/results/max_snow_values/'
    iPath_2 = 'D:/Churyulin/DON/results/all_year_plots/' #Путь к комплексному графику 1 за весь год
    #iPath_complex_1 = 'D:/Churyulin/DON/results/complex_1/'#Путь к комплексному графику за зимний сезон
    iPath_complex_1 = 'D:/Churyulin/DON/results/complex_3/'

    #iPath_complex_2 = 'D:/Churyulin/DON/results/complex_2/'
    iPath_complex_2 = 'D:/Churyulin/DON/results/complex_4/'

    # Cleaning previous results:
    l4s.clean_history(iPath_2)
    l4s.clean_history(iPath_complex_1)
    l4s.clean_history(iPath_complex_2)
    l4s.clean_history(iPath_max_snow)


    data_max_swe = []
    data_max_sd = []
    data_max_sd_st = []
    date = []
    index_station = []

    ocadki_dek_12 = [] # Список для суммы осадков за декаду
    ocadki_sez_12 = [] # Список для суммы осадков за сезон
    t_start_list = []  # Список для даты начала декады
    t_stop_list = [] #Список для даты конца декады


    dirs_csv = os.listdir(iPath)
    for file in sorted(dirs_csv):
        try:
            # Get data:
            # SYNOP dataset:
            df = l4p.get_csv_data(iPath + file)

            # SnoWE dataset:
            #df_snowe = pd.read_csv(iPath_snowe + f'000{file[0:5]}.txt', separ = ' ')
            df_snowe = l4p.get_csv_data(iPath_snowe + f'000{file[0:5]}.csv')

            # Snow survey (field, forest):
            df_field_survey = l4p.get_csv_data(iPath_field + file)
            df_forest_survey = l4p.get_csv_data(iPath_forest + file)

        except FileNotFoundError as error:
            print ( 'Exception: ', error )
            

        #-- Create time filter (winter values):
        if ltime_decade is True:
            periods = l4tp.get_decade_time_periods(
                np.arange(ref_date1, ref_date2, years2add), months)
            n_periods = len(periods)
        else:
            periods = l4tp.get_time_periods(
                ref_date1, ref_date2, n_periods, years2add)
            
        #-- Apply time filter:
        for tr in range(n_periods):
            y_w_1 = periods[tr][0]
            y_w_2 = periods[tr][1]

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
            
            # Данные по модели SnoWE (Snow depth, Snow density, SWE)
            snowe_sd = df_snowe['depth'][y_w_1:y_w_2]
            snowe_swe = df_snowe['swe'][y_w_1:y_w_2]
            snowe_rho = df_snowe['rho'][y_w_1:y_w_2]
            
            # Данные полевых  и лесных снегомерных маршрутов (SWE, RHO)
            field_in_situ = df_field_survey['swe'][y_w_1:y_w_2]
            forest_in_situ = df_forest_survey['swe'][y_w_1:y_w_2]

            field_in_situ_rho = df_field_survey['rho'][y_w_1:y_w_2]
            forest_in_situ_rho = df_forest_survey['rho'][y_w_1:y_w_2]

            #Блок максимальных значений по модели
            data_max_swe.append(snowe_swe.max())
            data_max_sd.append(snowe_sd.max())
            date.append(snowe_swe.idxmax())
            index_station.append(ts_index_st.mean())
            data_max_sd_st.append(ts_hsnow_w.max())
            ocadki_dek_12.append(ts_R12_w.sum())
            t_start_list.append(y_w_1)
            t_stop_list.append(y_w_2)

            df_max_snow = pd.concat(
                [
                    pd.Series(index_station, index = date),
                    pd.Series(data_max_swe, index = date),
                    pd.Series(data_max_sd, index = date),
                    pd.Series(ocadki_dek_12, index = date),
                    pd.Series(t_start_list, index = date),
                    pd.Series(t_stop_list, index = date),
                ], axis = 1
            )

            df_max_snow.columns = ['index','swe','sd', 'Sum_ocadkov','t_start','t_stop']

            df_max_snow.to_csv(iPath_max_snow + 'snow_max_dekada' + '.csv', sep=';', float_format='%.3f')


            #Работа с формой для комплексного графика
            rcParams['figure.subplot.left'] = 0.1  # Левая граница
            rcParams['figure.subplot.right']= 0.95  # Правая граница
            rcParams['figure.subplot.bottom']= 0.1  # Нижняя граница
            rcParams['figure.subplot.top'] = 0.95  # Верхняя граница
            rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots

            # Отрисовка комплексного графика 1
            if lcompex == 1:
                
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

                try:
                    temperatura = plot_2(
                        w_ax1, ts_t2m_w, ts_t2m_w_negative, n_1, n_2, n_3, n_4,
                        -30, 31, 15, l_p, y_w_1, y_w_2
                        )
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in temperatura: ', error )

                # График для температуры поверхности почвы: tming - минимальная температура поверхности почвы (град С)
                #t_g - температура поверхности почвы (град С)       
                na_1 = '3' #температура почвы
                na_2 = '4' #минимальная температура почвы
                na_3 = u'II' # графики для температуры поверхности почвы и минимальной температуры поверхности почвы
                na_4 = u'Температура, С'
                l_p = 'lower left'
                try:
                    soil_temp = plot_2(
                        w_ax2, ts_t_g_w, ts_tming_w, na_1, na_2, na_3, na_4,
                        -30, 31, 15, l_p, y_w_1, y_w_2)

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
                try:
                    precipitation_12 = bar_char_prec_1(
                        w_ax3, ts_R12_solid, ts_R12_liquid, name_001, name_002,
                        name_003, name_004, 0, up_R12, step_R12, l_p, y_w_1, y_w_2
                        )
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
                    snow_24 = bar_char_1(
                        w_ax4, ts_hsnow_w, name_0001, name_0002, name_0003,
                        start_sd, up_snow_sd, step_sd, l_p, colo, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception R12: ', error )
                plt.savefig(
                    iPath_complex_1 + 'Complex schedule_1_'+file[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2),
                    format='png', dpi = 300)
                plt.gcf().clear()

                
            #Отрисовка комплексного графика 2
            if lcompex == 2:
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
                try:
                    temperatura = plot_2(
                        w_bx1, ts_t2m_w, ts_t2m_w_negative, name_1, name_2,
                        name_3, name_4, -30, 31, 15, l_p, y_w_1, y_w_2)
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
                try:
                    precipitation_12 = bar_char_prec_1(
                        w_bx2, ts_R12_solid, ts_R12_liquid, name_001, name_002,
                        name_003, name_004, 0, up_R12, step_R12, l_p, y_w_1, y_w_2
                    )
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
                    snow_24 = bar_char_2(
                        w_bx3, ts_hsnow_w, snowe_sd, name_0001, name_0004,
                        name_0002, name_0003, start_sd, up_snow_sd, step_sd,
                        l_p, colo, y_w_1, y_w_2
                        )
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
                    snowe_info = plot_3_snow(
                        w_bx4, snowe_swe, field_in_situ, forest_in_situ, nam_1,
                        nam_2, nam_3, nam_4, nam_5, start_swe, up_snow_swe,
                        step_swe, l_p, y_w_1, y_w_2
                    )
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
                    snowe_rho = plot_3_snow(
                        w_bx5, snowe_rho, field_in_situ_rho*1000,
                        forest_in_situ_rho*1000, name_r_1, name_r_2, name_r_3,
                        name_r_4, name_r_5, start_rho, up_snow_rho, step_rho,
                        l_p, y_w_1, y_w_2)
                except (ValueError, TypeError)  as error:
                    print ( 'Exception in td2m: ', error )

                    plt.savefig(iPath_complex_2 + 'Complex schedule_2_'+ file[0:5]+' time_{}_{}.png'.format(y_w_1,y_w_2), format='png', dpi = 300)
                    plt.gcf().clear()


