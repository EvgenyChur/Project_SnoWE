# -*- coding: utf-8 -*-
"""
Description: Программа предназначена для обработки и сравнения данных с 
             метеостанций для проекта с Инной Крыленко по станциям на удельных 
             водосборах реки Северная Двина

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    08.02.2019 Evgenii Churiulin, RHMC
           Initial release
    1.2    24.04.2023 Evgenii Churiulin, MPI-BGC
           Prepered updated version. Script was fully rewritten  
"""

#=============================     Import modules     ==========================
# 1.1: Standard modules
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

# -- Import personal modules:
import lib4system_suport    as l4s
import lib4processing       as l4p
import lib4visualization    as l4v
import lib4time_periods     as l4tp
import lib4statistical_calc as l4stat

#=============================   Personal functions   =========================                                                       
def get_statistic(
        df_list:list, lst4delta:list, refer:str, t1:str, t2:str, 
        lfield_stations:bool, lforest_stations:bool):
    '''
    Task: Statistical analysis for snow data

    Parameters
    ----------
    df_list : Dataframe --> Research dataframes.
    lst4delta : Str --> Research parameters
    refer : --> Reference data
    t1, t2 : timesteps
    lfield_stations : Do you want to calculate statistic for field stations?
    lforest_stations : Do you want to calculate statistic for forest stations?

    Returns
    -------
    df_statistic : Dataframe --> Dataframe with statistical information.

    ''' 
    # Select SnoWE, ECOMAG and field survey data
    if lfield_stations is True:
        df_data_stat = pd.concat(df_list[0:7][t1:t2], axis = 1)
    # Select forest stations:
    if lforest_stations is True:
        df_data_stat = pd.concat(
            (df_list[0:6][t1:t2] + df_list[7:][t1:t2])[0:7], axis = 1)
    
    # Rename columns
    new_columns = lst4delta + [refer]               
    for i in range(len(list(df_data_stat.columns.values))):
        df_data_stat = df_data_stat.rename(
            columns = {
                list(df_data_stat.columns.values)[i]:new_columns[i]
                }
            )
                                        
    # Clean NaN values (by field)
    if lfield_stations is True:
        df_data_stat = df_data_stat[np.isfinite(df_data_stat[refer])]
    # Clean NaN values (by forest)
    if lforest_stations is True:
        df_data_stat = df_data_stat.dropna(axis = 'rows',thresh = 3)                      
                    
    # Calculation statistical parameters:
    try:
        df_statistic = l4stat.cal_stat_values(df_data_stat, lst4delta, refer)
        #  Save as a new output .csv file
        t1_out = str(t1)[0:11]
        t2_out = str(t2)[0:11]
        
        df_statistic.to_csv(
            f'{pout_stat}/{id_station}_{t1_out}_{t2_out}.csv',
            sep=';', float_format = '%.3f',
            #header = ['snowe','eco_model','eco_stat','field'],
            #index_label = 'Date',
            )                   
    except NameError as error:
        print ('Exception in field stations: ', error)
    
    return df_statistic
 
def cal_coef(df_model1, df_model2, df_model3, t2m, pout_csv):
    '''
    Task: Calculations of correction coefficient for SnoWE and ECOMAG data

    Parameters
    ----------
    df_model1 : Series
        Data from model 1.
    df_model2 : Series
        Data from model 2.
    df_model3 : Series
        Reference data
    t2m : Series
        Reference SYNOP data with T2m
    pout_csv : str
        Output path.

    Returns
    -------
    df_data_koef : Dataframe
        Table with coefficients.
    '''
    # Local variables:
    name4k_model = 'k_eco_cosmo'
    name4in_situ = 'k_eco_meteo'
    name4t2m = 't2m'
                
    #Поправочный коэффициент для модели COSMO-Ru (глобальной)
    k_model   = df_model1 / df_model2 
                
    #Поправочный коэффициент для ecomag счет по станциям
    k_in_situ = df_model1 / df_model3 
                
    # Create new Dataframe
    df_data_koef = pd.concat([k_model, k_in_situ, t2m], axis = 1)
    df_data_koef.columns = [name4k_model, name4in_situ, name4t2m]
                
    df_data_koef.to_csv(
        pout_csv, 
        sep = ';',
        float_format = '%.3f',
        header = [name4k_model,name4in_situ,name4t2m], 
        index_label = 'Date'
    )
    
    return df_data_koef

   
#================   User settings (have to be adapted)  =======================
# Logical parameters:
lprep_calc       = True  # Do you want to preprocess data for work?
lmain_calc       = True  # Do you want to make main calculations?
lstat_calc       = True  # Do you want to calculate statistical analysis?
lfield_stations  = True  # Do you want to calculate script with field snow survey data? 
lforest_stations = False # Do you want to calculate script with forest snow survey data? 
lvisual          = True  # Do you want to create plots?
lrecal_coef      = True  # Do you want to get recalculation coeeficients?

# Main path for working with input and output data
main = 'D:/Churyulin/snow data(ivan)'

# Preprosessing initial data (lprep_calc = True, lmain_calc = False)
if lprep_calc is True:
    # Input info:
    pin_catalog = [
    #                Input data paths:                   Type                  Данные:
        [main + '/inna_data/snow_ecomag_new.csv'      , 'eco'],                # ECOMAG счет по COSMO
        [main + '/inna_data/snow_meteostation_new.csv', 'eco'],                # ECOMAG счет по станциям
        [main + '/inna_data/snow_hybrid_new.csv'      , 'eco'],                # ECOMAG счет по COSMO с региональной СУД
        [main + '/inna_data/snow_cosmo_koef.csv'      , 'eco'],                # ECOMAG счет по COSMO с поправочными коэффициентами
        [main + '/inna_data/snow_meteo_koef.csv'      , 'eco'],                # ECOMAG счет по метеостанциям с поправочным коэффиентом 
        [main + '/result_filter/field.csv'            , 'obs'],                # с маршрутными снегомерными наблюдениями в поле - станции
        [main + '/result_filter/forest.csv'           , 'obs'],                # с маршрутными снегомерными наблюдениями в лесу
    ]
    # Output info:
    pout_catalog = [
    #                 Output data paths:                                       Результаты
        main + '/inna_data_ecomag/',                                           # ECOMAG счет по космо]
        main + '/inna_data_meteostation/',                                     #  ECOMAG счет по станциям# 
        main + '/inna_data_hybrid/',                                           # ECOMAG счет по COSMO с региональной СУД
        main + '/inna_data_cosmo_koef/',                                       # ECOMAG счет по COSMO с поправочными коэффициентами
        main + '/inna_data_meteo_koef/',                                       # ECOMAG счет по метеостанциям с поправочным коэффиентом 
        main + '/inna_meteo_field/',                                           # с маршрутными снегомерными наблюдениями в поле - станции
        main + '/inna_meteo_forest/',                                          # с маршрутными снегомерными наблюдениями в лесу
    ]
        
    # Cleaning previous results:
    for path in pout_catalog:
        l4s.cleah_history(path)
        
    # List of meteorological station for research (SYPON) -> 
    # (change ECOMAD stations to current values)
    lst4station = [
        22563, 23608, 23701, 23709, 22671, 22676, 22557, 23704, 22559, 23803, 23707,
        22781, 22651, 22656, 22798, 23804, 23808, 22762, 22778, 22657, 23807, 22876,
        22768, 23904, 22889, 22887, 22888, 22996, 22983, 22869, 22981, 27083, 22988,
        22867, 22974, 22966, 27071, 27066, 27051, 27044, 27026, 27037
    ]
    
# Main calculations. (lprep_calc = False, lmain_calc = True)
if lmain_calc is True:
    # Stations for analysis:
    
    # Option 1 (North Dvina catchment area):
    lst4station = [
        22563, 22656, 22671, 22762, 22778, 22798, 22867, 22974, 22768, 22981,
        22876, 23803, 22996, 23701, 23709, 23804, 23807, 23904, 27051, 27066,
        27083]
    
    #-- Option 2:
    #lst4station = [
    #    22563, 22671, 22762, 22768, 22778, 22798, 22867, 22974, 22996, 23701,
    #    23709, 23803, 23804, 23807, 27051, 27066, 27083, 22876, 23904]
    
    #-- Option 3 (Best scores for SNOWE):
    #lst4station = [
    #    22563, 22762, 22768, 22798, 22867, 22974, 22996, 27051, 27083, 22876] 
    
    #-- Option 4 (Best scores for ECOMAG):
    #lst4station = [
    #    22671, 22778, 23701, 23709, 23803, 23804, 23807, 27066, 23904]
     
    #-- Option 5 (full list of stations):
    #lst4station = [
    #    22557, 22559, 22563, 22651, 22656, 22657, 22671, 22676, 22762, 22768, 
    #    22778, 22781, 22798, 22867, 22869, 22876, 22887, 22888, 22889, 22966,
    #    22974, 22981, 22983, 22988, 22996, 23608, 23701, 23704, 23707, 23709,
    #    23803, 23804, 23807, 23808, 23904, 27026, 27037, 27044, 27051, 27066,
    #    27071, 27083]      
    
    # Input info:
    pin_catalog = {}
    for id_station in sorted(lst4station):
        pin_catalog[id_station] = [
        #                  Input data paths                       Type         Данные:
            [main + f'/inna_snowe_result/000{id_station}.txt'  , 'snowe'],     # из SnoWE                                                iPath_snowe
            [main + f'/inna_data_ecomag/{id_station}.csv'      , 'eco'  ],     # ECOMAG счет по COSMO                                    iPath_1
            [main + f'/inna_data_meteostation/{id_station}.csv', 'eco'  ],     # ECOMAG счет по станциям                                 iPath_2
            [main + f'/inna_data_hybrid/{id_station}.csv'      , 'eco'  ],     # ECOMAG счет по COSMO с региональной СУД                 iPath_5 
            [main + f'/inna_data_cosmo_koef/{id_station}.csv'  , 'eco'  ],     # ECOMAG счет по COSMO с поправочными коэффициентами      iPath_7 
            [main + f'/inna_data_meteo_koef/{id_station}.csv'  , 'eco'  ],     # ECOMAG счет по метеостанциям с поправочным коэффиентом  iPath_6
            [main + f'/inna_meteo_field/{id_station}.csv'      , 'obs'  ],     # с маршрутными снегомерными наблюдениями в поле          iPath_3
            [main + f'/inna_meteo_forest/{id_station}.csv'     , 'obs'  ],     # с маршрутными снегомерными наблюдениями в лесу          iPath_4
            [main + f'/inna_meteo_1day/{id_station}.csv'       , 'sypon'],     # из SYPON (snow depth)                                   iPath_test
            [main + f'/inna_meteo_1day/{id_station}.csv'       , 'synop'],     # из Sypon (temperature) iPath_44 = ],
        ]    
    
    # Output folders:
    pout_data = main + '/result_data'
    pout_stat = main + '/statistica'
    pout_plot = main + '/inna_comparison_plot'        
    
    # Create output folders:
    pout_data = l4s.makefolder(pout_data)
    pout_stat = l4s.makefolder(pout_stat) 
    pout_plot = l4s.makefolder(pout_plot)

    # Cleaning previous results:
    l4s.cleah_history(f'{pout_plot}/')
    
    # --          Option 1      Option 2      Option 3        
    ref_date1 = '2011-09-01' # '2013-09-01' #'2013-09-01'
    ref_date2 = '2012-06-30' # '2014-06-30' #'2018-05-31'
    n_periods = 7            #     5             1
    years2add = 1            #     1             5    
    
    # Settings for field and forest snow survey
    lst4delta = ['snowe_swe'    , 'ecomag_model'     , 'ecomag_meteo'     , 
                 'ecomag_hybrid', 'ecomag_cosmo_koef', 'ecomag_meteo_koef']
    if lfield_stations is True:
        refer = 'field'
    if lforest_stations is True:
        refer = 'forest'        
    
    
    # User settings:
    ws =  1.0 # line size
    ms = 50.0 # marker size
    
    lst4plot_settings = {
        # Uniq settings for plot with 4 lines:
        'plot4' : {
            # Plot type ('line', 'scatter')
            'mode' : ['line', 'line', 'scatter', 'scatter'],     
            # Legend  (SnoWE, SYPON, полевые u лесные снегомерные маршруты)
            'label' : ['SnoWE', 'SYNOP', 'OBS (field)', 'OBS (forest)'],
            # line colors
            'color'  : ['blue', 'black', 'black', 'black'],
            # line style   (if 'mode' = 'scatter' -> not active)
            'lstyle' : [  '-' ,   '-'  ,    ''  ,   ''   ],
            # line wight   (if 'mode' = 'scatter' -> not active)
            'wstyle' : [   ws ,   ws   ,    ws  ,     ws ],
            # marker style (if 'mode' = 'line'    -> not active)
            'mstyle' : [  ''  ,   ''   ,     '^',   'o'  ],
            # marker size  (if 'mode' = 'line'    -> not active)
            'msize'  : [   ms ,   ms   ,    ms  ,     ms ],                                    
        },
        # Uniq settings for plot with 5 lines:
        'plot5' : {
            'mode' : ['line', 'line', 'line', 'scatter', 'scatter'],           
            # Legend labels (SnoWE, Ecomag с: _COSMO, _станциям, полевые u лесные снегомерные маршруты)
            'label' : [
                'SnoWE', 'ECOMAG COSMO', 'ECOMAG OBS', 'OBS (field)', 'OBS (forest)'],
            # line colors
            'color'  : ['blue', 'red', 'red',  'black', 'black'],
            # line style   (if 'mode' = 'scatter' -> not active)
            'lstyle' : [  '-' ,   '-',  '--',     ''  ,   ''   ],
            # line wight   (if 'mode' = 'scatter' -> not active)
            'wstyle' : [   ws ,   ws ,    ws,     ws  ,    ws  ],
            # marker style (if 'mode' = 'line'    -> not active)
            'mstyle' : [  ''  ,   '' ,    '',     '^' ,   'o'  ],
            # marker size  (if 'mode' = 'line'    -> not active)
            'msize'  : [   ms ,   ms ,    ms,     ms  ,    ms  ],
        },
        # Uniq settings for plot with 6 lines:
        'plot6' : {
            'mode' : ['line', 'line', 'line', 'scatter', 'scatter', 'line'],         
            # Legend labels
            'label' : [
                'SnoWE',               # SnoWE
                'ECOMAG COSMO',        # Ecomag расчет по COSMO
                'ECOMAG OBS',          # Ecomag расчет по stations
                'OBS (field)',         # полевые снегомерные маршруты
                'OBS (forest)',        # лесные снегомерные маршруты
                'ECOMAG COSMO hybrid', # Ecomag расчет по гибридной COSMO (snowe correction)
                ],
            # line colors
            'color'  : ['blue', 'red', 'red',  'black', 'black', 'red'],
            # line style   (if 'mode' = 'scatter' -> not active)
            'lstyle' : [  '-' ,   '-',  '--',     ''  ,   ''   ,  '--'],
            # line wight   (if 'mode' = 'scatter' -> not active)
            'wstyle' : [   ws ,   ws ,    ws,     ws  ,    ws  ,   ws ],
            # marker style (if 'mode' = 'line'    -> not active)
            'mstyle' : [  ''  ,   '' ,    '',     '^' ,   'o'  ,   '' ],
            # marker size  (if 'mode' = 'line'    -> not active)
            'msize'  : [   ms ,   ms ,    ms,     ms  ,    ms  ,   ms ],
        },
        
        # Uniq settings for plot with 7 lines:
        'plot7' : {
            'mode' : ['line', 'line', 'line', 'line', 'line', 'scatter', 'scatter'],         
            # Legend labels
            'label' : [
                'SnoWE',             # SnoWE
                'ECOMAG COSMO',      # Ecomag расчет по COSMO
                'ECOMAG COSMO_corr', # Ecomag расчет по COSMO с поправочным коэффициентом
                'ECOMAG OBS',        # Ecomag расчет по stations
                'ECOMAG OBS_corr',   # Ecomag расчет по stations с поправочным коэффициентом
                'OBS (field)',       # полевые снегомерные маршруты
                'OBS (forest)',      # лесные снегомерные маршруты
                ],
            # line colors
            'color'  : ['blue', 'red', 'red', 'green', 'green', 'black', 'black'],
            # line style   (if 'mode' = 'scatter' -> not active)
            'lstyle' : [  '-' ,   '-',  '--',   '-'  ,  '--'  ,    ''  ,   ''   ],
            # line wight   (if 'mode' = 'scatter' -> not active)
            'wstyle' : [   ws ,   ws ,    ws,     ws ,    ws  ,    ws  ,    ws  ],
            # marker style (if 'mode' = 'line'    -> not active)
            'mstyle' : [  ''  ,   '' ,    '',    ''  ,    ''  ,    '^' ,   'o'  ],
            # marker size  (if 'mode' = 'line'    -> not active)
            'msize'  : [   ms ,   ms ,    ms,     ms ,    ms  ,    ms  ,    ms  ],                                              
        },
        
        # -- Common settings for all plots:
        # legend location
        'l_location' : 'upper left',
        # x axis label (common for all. Was turned off)
        'x_label'    : 'X axis label was turned off',
        # format of axis by x axis (time or values) - ['%H', '%Y-%m-%d', '%Y' '%B' '%d-%m' %m-%d]
        'xformat'    : ['time', '%Y-%m'],
        # xmin, xmax, xstep values or time  (xmin and xmax will be define later)
        'xlimits'    : ['', '', '1M'],
        # rotation of numbers by X axis (deg)
        'rotation'   : 0.0,
        # size of numbers for X and Y axes
        'fsize'      : 14.0,
        
        # Settings for snow depth plot:     
        'sd_plot' : {
            'plt_label'  : 'Snow depth',              # plot title,
            'y_label'    : 'Snow depth, sm',           # y axis label
            'ylimits'    : [0.0, 151.1, 25],           # ymin, ymax, ystep values or time
        },
        # Settings for snow density plot:
        'swe_plot' : {
            # Settings for labels:
            'plt_label'  : 'Snow water equivalent',
            'y_label'    : 'Snow water equivalent, mm',
            'ylimits'    : [0.0, 301.1, 50.0],
        }, 
    }
    
    param = 'swe'
    
#=============================    Main program   ==============================

# Подготовительная стадия. Цель подготовить исходные данные для работы
if lprep_calc is True:  
    # Reading data:
    for i in range(len(pin_catalog)):
        # 0 - path; 1 - data type
        if pin_catalog[i][1] == 'eco':
            l4p.get_ecomag_data(pin_catalog[i][0], lst4station, pout_catalog[i])
        else:
            l4p.get_obs_data(pin_catalog[i][0], pout_catalog[i])

# Основная часть работы. Работа с данными и отрисовка материалов.
if lmain_calc is True:
    
    # Start calculations for station
    for id_station in sorted(lst4station):
        
        #-- Get data from all data sources for one station:
        data4station = []                                                      # List of data for one station
        lst4pin = pin_catalog.get(int(id_station))
        for i in range(len(lst4pin)):
            # lst4pin[i][0] -> input path; lst4pin[i][1] -> input type
            if lst4pin[i][1] == 'snowe':
                data4station.append(l4p.get_csv_data(lst4pin[i][0], ' '))
            else:
                data4station.append(l4p.get_csv_data(lst4pin[i][0]))

        #-- Create time filter (winter values):   
        periods = l4tp.get_time_periods(
            ref_date1, ref_date2, n_periods, years2add)    
    
        #-- Apply time filter (winter values):
        winter_data4station = []
        for i in range(len(data4station)):
            for t in range(n_periods):
                # -- Select time range (t1 - start; t2 - stop)
                t1 = periods[t][0]
                t2 = periods[t][1]
                winter_data4station.append(data4station[param][t1:t2])
        
        # Статистическая обработка данных для полевых метеостанций.
        if lstat_calc is True:
            for i in range(len(winter_data4station)):
                for t in range(n_periods):
                    # -- Select time range (t1 - start; t2 - stop)
                    t1 = periods[t][0]
                    t2 = periods[t][1]
                    # Select SnoWE, ECOMAG and field survey data
                    if lfield_stations is True:
                        df_stat_field = get_statistic(
                            winter_data4station, lst4delta, refer, t1, t2, 
                            lfield_stations, lforest_stations)
                    # Select forest stations: 
                    if lforest_stations is True:
                        df_stat_field = get_statistic(
                            winter_data4station, lst4delta, refer, t1, t2, 
                            lfield_stations, lforest_stations)  
        # End of Statistic section
             
        # Блок визуализации результатов
        if lvisual is True:
            for i in range(len(winter_data4station)):
                for t in range(n_periods):
                    # -- Select time range (t1 - start; t2 - stop)
                    t1 = periods[t][0]
                    t2 = periods[t][1]            
                    
                    # -- Define time settings for x axis
                    lst4plot_settings.get('xlimits')[0] = t1 # xmin
                    lst4plot_settings.get('xlimits')[1] = t2 # xmax
                    
                    # -- Create plots:
                    # SWE plot
                    fig = plt.figure(figsize = (14,10))
                    ax = fig.add_subplot(111)
                    try:
                        l4v.create_plot(ax, winter_data4station[i], set4plots, plot_type, 'swe_plot', 'plot7')
                        #l4v.create_plot(ax, winter_data4station[i], set4plots, plot_type, 'swe_plot', 'plot6')      
                        #l4v.create_plot(ax, winter_data4station[i], set4plots, plot_type, 'swe_plot', 'plot5')
                        # -- Save plot:
                        t1_out = str(t1)[0:11]
                        t2_out = str(t2)[0:11]
                        
                        plt.savefig(
                            f'{pout_plot}/plot_swe_{t1_out}_{t2_out}.png',
                            format = 'png',
                            dpi = 300
                        ) 
                        plt.gcf().clear()   
                        
                    except NameError as error:
                        print ( 'Exception: Problem with visualization - SWE. ', error )

                    # SD plot
                    fig = plt.figure(figsize = (14,10))
                    bx = fig.add_subplot(111)   
                    
                    try:
                        l4v.create_plot(ax1, [snowe_sd, in_situ_sd, field_sd, forest_sd,], set4plots, plot_type, script)
                        # -- Save plot:
                        t1_out = str(t1)[0:11]
                        t2_out = str(t2)[0:11]
                        plt.savefig(
                            f'{pout_plot}/plot_sd_{t1_out}_{t2_out}.png',
                            format = 'png',
                            dpi = 300
                        ) 
                        plt.gcf().clear()
                    except NameError as error:
                        print ( 'Exception: Problem with visualization - SD. ', error )      
        # End of visualization section
        
        
        # Section: Calculating recalculation coefficients.
        if lrecal_coef is True:
            for t in range(n_periods):
                # -- Select time range (t1 - start; t2 - stop)
                t1 = periods[t][0]
                t2 = periods[t][1]   
                        
                # -- Output settings:
                t1_out = str(t1)[0:11]
                t2_out = str(t2)[0:11]
                pout_csv = f'{pout_data}/{id_station}_{t1_out}_{t2_out}.csv'
                try:    
                    df_data_koef = cal_coef(
                        winter_data4station[0][t1:t2],  # SnoWE
                        winter_data4station[1][t1:t2],  # ECOMAG COSMO
                        winter_data4station[2][t1:t2],  # ECOMAG stations
                        winter_data4station[-1][t1:t2], # T2M
                        pout_csv) 
                except NameError as error:
                    print ('Exception: Recalculation coefficient.', error) 
        # end of section  
    # end of calculations for station
        