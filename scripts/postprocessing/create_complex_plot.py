# -*- coding: utf-8 -*-
"""
Description: Скрипт предназначен для отрисовки графиков на основе
             метеорологических данных за временныv интервалы. В текущей версии 
             работа скрипта фокусируется на обработке данных с метеостанции
             располагающихся в Москве и Московской области. Скрипт может быть
             переделан для любого водосбора, путем изменения путей к исходным
             данным;

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    11.09.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    24.04.2023 Evgenii Churiulin, MPI-BGC
           Updating script 
"""

#=============================     Import modules     ======================
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams

# -- Import personal modules:
import lib4system_suport    as l4s
import lib4processing       as l4p
import lib4visualization    as l4v
import lib4time_periods     as l4tp

#=============================   Personal functions   =========================

#================   User settings (have to be adapted)  =======================

# User settings for time filter:
# --          Option 1      Option 2      Option 3        
ref_date1 = '2011-10-01' # '2010-10-01' #'2011-01-01'
ref_date2 = '2012-04-30' # '2001-04-30' #'2012-12-31'
n_periods = 7            #     18       #     5
years2add = 1            #     1        #     1  


# User settings for plots:
ws =  1.0 # line size
ms = 50.0 # marker size
    
lst4plot_settings = {
    # Uniq settings for plot with 1 lines (Precipitations for 24 hours):
    'plot1_prec24' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['bar'     ],
        'label'  : ['precip 24 hour'],
        'color'  : ['green'    ],
        'lstyle' : [  '-'      ],
        'wstyle' : [   ws      ],
        'mstyle' : [  ''       ],
        'msize'  : [   ms      ],
    },
    
    # Uniq settings for plot with 1 lines (Precipitations for 12 hours):
    'plot1_prec12' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['bar'     ],
        'label'  : ['precip 12 hour'],
        'color'  : ['green'    ],
        'lstyle' : [  '-'      ],
        'wstyle' : [   ws      ],
        'mstyle' : [  ''       ],
        'msize'  : [   ms      ],
    },    
    
    # Uniq settings for plot with 1 lines (Snow depth):
    'plot1_snow_sd' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['bar'       ],
        'label'  : ['Snow depth'],
        'color'  : ['blue'      ],
        'lstyle' : [  '-'       ],
        'wstyle' : [   ws       ],
        'mstyle' : [  ''        ],
        'msize'  : [   ms       ],
    }, 
    # Uniq settings for plot with 1 lines (Dew point):
    'plot1_dew' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['line'     ],
        'label'  : ['dew point'],
        'color'  : ['black'    ],
        'lstyle' : [  '-'      ],
        'wstyle' : [   ws      ],
        'mstyle' : [  ''       ],
        'msize'  : [   ms      ],
    },
    
    # Uniq settings for plot with 1 lines (Wind):
    'plot1_wind' : {
        'mode'   : ['line'  ],
        'label'  : ['U wind'],
        'color'  : ['black' ],
        'lstyle' : [  '-'   ],
        'wstyle' : [   ws   ],
        'mstyle' : [  ''    ],
        'msize'  : [   ms   ],
    },
    'plot2_wind' : {
        'mode'   : ['line'  , 'line'],
        'label'  : ['U wind mean', 'U wind max'],
        'color'  : ['black' , 'black'],
        'lstyle' : [  '-'   , '--'],
        'wstyle' : [   ws   , ws],
        'mstyle' : [  ''    , ''],
        'msize'  : [   ms   , ms],
    },
    # Uniq settings for plot with 2 lines (Soil temperature):
    'plot2_soil' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['line'     , 'line'         ],
        'label'  : ['soil temp', 'min soil temp'],
        'color'  : ['black'    , 'black'        ],
        'lstyle' : [  '-'      ,   '--'         ],
        'wstyle' : [   ws      ,   ws           ],
        'mstyle' : [  ''       ,   ''           ],
        'msize'  : [   ms      ,   ms           ],
    }, 
    
    # Uniq settings for plot with 2 lines (Air pressure):
    'plot2_pres' : {
        # Plot type ('line', 'scatter')
        'mode'   : ['line', 'line'],
        'label'  : ['air ps station level', 'air ps sea level'],
        'color'  : ['black', 'black'],
        'lstyle' : [  '--' ,   '-'  ],
        'wstyle' : [   ws ,   ws    ],
        'mstyle' : [  ''  ,   ''    ],
        'msize'  : [   ms ,   ms    ],
    },     
    
    # Uniq settings for plot with 3 lines (Temperatures):
    'plot3' : {
        # Plot type ('line', 'scatter')
        'mode' : ['line', 'line', 'line'],
        # Legend
        'label' : ['Tmax_2M', 'T_2M', 'Tmin_2M'],
        # line colors
        'color'  : ['black', 'black', 'black'],
        # line style   (if 'mode' = 'scatter' -> not active)
        'lstyle' : [  '--' ,   '-'  ,    ':' ],
        # line wight   (if 'mode' = 'scatter' -> not active)
        'wstyle' : [   ws ,   ws    ,    ws   ],
        # marker style (if 'mode' = 'line'    -> not active)
        'mstyle' : [  ''  ,   ''    ,     ''  ],
        # marker size  (if 'mode' = 'line'    -> not active)
        'msize'  : [   ms ,   ms    ,    ms   ],
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
    
    # Uniq settings for plots:     
    't2m_plot' : {
        'plt_label'  : 'Температура воздуха',
        'y_label'    : 'Температура, С',
        'ylimits'    : [-30.0, 30.1, 15],
    },            
    'tsoil_plot' : {
        'plt_label'  : 'Температуры поверхности почвы',
        'y_label'    : 'Температура, С',
        'ylimits'    : [-30.0, 31.1, 15],
    },
    'dew_plot' : {
        'plt_label'  : 'Температура точки росы',
        'y_label'    : 'Температура, С',
        'ylimits'    : [-30.0, 31.1, 15],
    },
    'air_plot' : {
        'plt_label'  : 'Атмосферное давление',
        'y_label'    : 'Атмосферное давление, гПа',
        'ylimits'    : [940.0, 1040.1, 20.0],
    },
    'prec_12': {
        'plt_label'  : 'Осадки за 12 часов',
        'y_label'    : 'Осадки, мм',
        'ylimits'    : [0.0, 30.0, 10.0],
    },
    'prec_24' : {
        'plt_label'  : 'Осадки за 24 часа',
        'y_label'    : 'Осадки, мм',
        'ylimits'    : [0.0, 70.1, 10.0],
    },
    'sd_plot' : {
        'plt_label'  : 'Высота снежного покрова',
        'y_label'    : 'Высота снега, см',
        'ylimits'    : [0.0, 60.1, 20.0],
    },
    'u_plot' : {
        'plt_label'  : 'Скорость ветра',
        'y_label'    : 'Скорость ветра, м/с',
        'ylimits'    : [0.0, 7.1, 1.0],
    },
    'w_plot' : {
        'labels' : ['wind direction'],
        'plt_label'  : 'Направление ветра',
        'y_label'    : 'Направление ветра, град',
        'ylimits'    : [0.0, 360.1, 72.0],
    },
}


#================   User settings (have to be adapted)  =======================
 
# Input and output paths:
pin  = 'D:/Churyulin/DV/result_1_month_2011_2019'
pout = 'D:/Churyulin/DV/result_plot_2011_2019'

# Select parameters for research:
params_opt = 'basic'

#=============================    Main program   ==============================
# Create output folder:
l4s.makefolder(pout)

# Cleaning previous results:
l4s.cleah_history(pout) 

for file in os.listdir(pin):
          
    # Get data from csv files:
    df = l4p.get_csv_data(f'{pin}/{file}')      
    print ('Columns:', df.columns)
        
    #Работа с формой для комплексного графика
    rcParams['figure.subplot.left']   = 0.1  # Левая граница
    rcParams['figure.subplot.right']  = 0.95 # Правая граница
    rcParams['figure.subplot.bottom'] = 0.1  # Нижняя граница
    rcParams['figure.subplot.top']    = 0.95 # Верхняя граница
    rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots

    #-- Create time filter (winter values):   
    periods = l4tp.get_time_periods(
        ref_date1, ref_date2, n_periods, years2add)  

    #-- Apply time filter (winter values):
    for k in range(n_periods):
        # -- Select time range (y1 - start; y2 - stop)
        y1 = periods[k][0]
        y2 = periods[k][1]
        
        y1_out = str(y1)[0:11]
        y2_out = str(y2)[0:11]
                        
        # -- Get parameters for complex plot:
        # ps - давление на уровне станции (гПа)
        ts_ps     = df['ps'][y1:y2]
        # pmsl - давление, приведенное к уровню моря (гПа)  
        ts_pmsl   = df['pmsl'][y1:y2]
        # t2m - температура воздуха (град С);
        ts_t2m    = df['t2m'][y1:y2]
        # td2m - температура точки росы (град С)
        ts_td2m   = df['td2m'][y1:y2]
        # dd10m - направления ветра (град) на высоте 10 метров
        ts_dd10m  = df['dd10m'][y1:y2]
        # tmin2m - минимальная температура воздуха (град С)
        ts_tmin2m = df['tMin2m'][y1:y2]
        # tmax2m - максимальная температура воздуха (град С) 
        ts_tmax2m = df['tMax2m'][y1:y2]
        # tming - минимальная температура поверхности почвы (град С)
        ts_tming  = df['tMinG'][y1:y2]
        # R12 - осадки за 12 часов, мм - RAINS 
        ts_R12    = df['R12'][y1:y2]
        # R24 - осадки за 24 часа, мм - RAINS 
        ts_R24    = df['R24'][y1:y2]
        # t_g - температура поверхности почвы (град С) 
        ts_t_g    = df['t_g'][y1:y2]
        # hsnow - 
        ts_hsnow  = df['hSnow'][y1:y2]
            
        if params_opt == 'basic':
            # ff10m - скорость ветра (м/сек) на высоте 10 метров
            ts_ff10m = df['ff10m'][y1:y2]
        
        if params_opt == 'full':
            # ff10mean - скорость ветра (м/сек) на высоте 10 метров (MEAN)
            ts_ff10mean = df['ff10meanm'][y1:y2]
            # ff10max - скорость ветра (м/сек) на высоте 10 метров (MAX)
            ts_ff10max  = df['ff10max'][y1:y2]           
            
            
        # -- Create the first complex plot:    
        fig = plt.figure(figsize = (14,10))
            
        #Задание координатной сетки и места где будут располагаться графики
        egrid = (4,4)
        ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
        ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
        ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
        ax4 = plt.subplot2grid(egrid, (3,0), colspan = 4)
        
        try:
            # График для температура воздуха: 
            l4v.create_plot(
                ax1, [ts_tmax2m, ts_t2m, ts_tmin2m], set4plots, 't2m_plot', 'plot3')       
            # График для температуры поверхности почвы: 
            l4v.create_plot(ax2, [ts_t_g, ts_tming], set4plots, 'tsoil_plot', 'plot2_soil')
            # График для температуры точки росы
            l4v.create_plot(ax3, [ts_td2m], set4plots, 'dew_plot', 'plot1_dew')            
            # График для давления:
            l4v.create_plot(ax4, [ts_ps, ts_pmsl], set4plots, 'air_plot', 'plot2_pres')
            
            # Save plot
            plt.savefig(
                f'{pout}/Complex_plot1_{file[0:5]}_{y1_out}_{y2_out}.png', 
                format = 'png', 
                dpi = 300)
            # Clear figure
            plt.gcf().clear()
            
        except NameError as error:
            print ( 'Exception: Complex plot - 1', error )    
        
        # -- Create the second complex plot:  
        fig2 = plt.figure(figsize = (14,10))
                
        #Задание координатной сетки и места где будут располагаться графики
        egrid_2 = (3,4)
        bx1 = plt.subplot2grid(egrid_2, (0,0), colspan = 4)
        bx2 = plt.subplot2grid(egrid_2, (1,0), colspan = 4)
        bx3 = plt.subplot2grid(egrid_2, (2,0), colspan = 4)   
        
        try:
            # График для осадков за 12 час, мм - RAINS 
            l4v.create_plot(bx1, [ts_R12], set4plots, 'prec_12', 'plot1_prec12')
            # График для осадков за 24 часа, мм - RAINS 
            l4v.create_plot(bx2, [ts_R24], set4plots, 'prec_24', 'plot1_prec24')
            #График для высоты снежного покрова, см
            l4v.create_plot(bx3, [ts_hsnow], set4plots, 'sd_plot', 'plot1_snow_sd')
            
            # Save plot
            plt.savefig(
                f'{pout}/Complex_plot2_{file[0:5]}_{y1_out}_{y2_out}.png',
                format='png',
                dpi = 300
            )
            # Clean figure
            plt.gcf().clear()  
            
        except NameError as error:
            print ( 'Exception: ', error )
            
        # -- Create the trird complex plot: 
        fig3 = plt.figure(figsize = (14,10))
            
        #Задание координатной сетки и места где будут располагаться графики
        egrid_3 = (2,4)
        cx1 = plt.subplot2grid(egrid_3, (0,0), colspan = 4)
        cx2 = plt.subplot2grid(egrid_3, (1,0), colspan = 4)
        
        try:
            # График для ff10m - скорость ветра (м/сек) на высоте 10 метров
            if params_opt == 'basic':
                l4v.create_plot(cx1, [ts_ff10m], set4plots, 'u_plot_basic', 'plot1_wind')
            if params_opt == 'full':
                l4v.create_plot(cx1, [ts_ff10mean, ts_ff10max], set4plots, 'u_plot_full', 'plot2_wind')
            
            l4v.create_plot(cx1, [ts_ff10mean, ts_ff10max], set4plots, 'u_plot_full', 'plot1_wind')
            
            # График для dd10m - направления ветра (град) на высоте 10 метров   
            l4v.create_plot(cx2, [ts_dd10m], set4plots, 'w_plot', 'plot1_wind')
            # Save plot                    
            plt.savefig(
                f'{pout}/Complex_plot3_{file[0:5]}_{y1_out}_{y2_out}.png',
                format='png',
                dpi = 300
                )
            # Clean figure
            plt.gcf().clear()
            
        except NameError as error:
            print ( 'Exception: ', error )

