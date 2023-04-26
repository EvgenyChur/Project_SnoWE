# -*- coding: utf-8 -*-
"""
Description: Script for preprocessing of data (snow depth, snow water equivalent,
             surface temperatures and precipitations) downloaded from METEO.RU 
             web-page.

Authors: Evgenii Churiulin,

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    02.12.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    15.03.2021 Evgenii Churiulin, CESR
           Created new version based on 'get_meteo_RU_data.sh'and 'get_meteo_RU_data 2.sh'
           Previuos scripts were deleted.
    1.3    25.04.2023 Evgenii Churiulin, MPI-BGC
           Created new version based on 'meteo_ru_soft.sh' and 'meteo_ru_plots.sh'
"""
# =============================     Import modules     =====================
# 1.1: Standard modules
import numpy as np
import pandas as pd
from matplotlib import rcParams
import matplotlib.pyplot as plt
# 1.2 Personal module
import lib4processing as l4p
import lib4system_suport as l4s
import lib4visualization as l4v
# =============================   Personal functions   =====================

# ================   User settings (have to be adapted)  ===================

# -- Logucal types for actual timesteps:
ldaily   = True  # Daily  time step interval ---> (True / False)
lmonthly = False # Montly time step interval ---> (True / False)
luser    = False # User   time step interval ---> (True / False)
lbox_plot = True

# -- Input and output paths:
pin  = 'C:/Users/Churiulin/Desktop/RSHU_ex'
pout = pin + 'results/'

# -- List of meteostations :  
#lst4stations = [
#    '22271', '22438', '22471', '22676', '22845', '22854', '22981', '23330',
#    '23412', '27051'
#]

lst4stations = ['22271']
lst4stations.sort()

# -- Set user time filter:
if ldaily is True:
    # -- Select time range (t1 - start; t2 - stop)
    t1 = pd.date_range(start =' 1960-01-01', end = '1960-01-02', freq = 'D')
    t2 = pd.date_range(start = '1960-01-02', end = '1960-01-03', freq = 'D')
    
if lmonthly is True:
    t1 = pd.date_range(start = '1990-10-01', end = '1995-06-01', freq = 'MS')
    t1 = pd.date_range(start = '1990-10-01', end = '1995-07-01', freq = 'M')

if luser is True:
    t1 = pd.to_datetime(
        ['1990-10-01', '1991-10-01', '1992-10-01', '1993-10-01', '1995-10-01'])
    t2 = pd.to_datetime(
        ['1991-06-01', '1992-06-01', '1993-06-01', '1994-06-01', '1996-06-01'])

# Step for mean values ('D' - daily, '2D', '3D')
step = 'D'

# Select river:
river_names = ['the Mezen river - s. Borovichi',
                'the Neva river - s. St.Petersburg']

# -- User plot settings:
ws = 1
ms = 50

lst4plot_settings = {
    # Uniq settings for plot with 3 lines:
    'plot3' : {
        # Plot type ('line', 'scatter', 'bar')
        'mode' : ['line'] * 3,
        # Legend
        'label' :  ['max T', 'avg T', 'min T'],
        # line colors
        'color'  : ['r', 'm', 'b'],
        # line style   (if 'mode' = 'scatter' -> not active)
        'lstyle' : [  '-' ,   '-.'  ,   '--' ],
        # line wight   (if 'mode' = 'scatter' -> not active)
        'wstyle' : [   ws ,   ws   ,    ws   ],
        # marker style (if 'mode' = 'line'    -> not active)
        'mstyle' : [  ''  ,   ''   ,     '', ],
        # marker size  (if 'mode' = 'line'    -> not active)
        'msize'  : [   ms ,   ms   ,    ms   ],
    },
    # Uniq settings for plot with 2 lines:
    'plot2_bar'  : {
        'mode'   : ['bar'] * 2,
        'label'  : ['solid', 'Liq'  ],
        'color'  : ['b', 'g'],
        'lstyle' : ['' , '' ],
        'wstyle' : [ws , ws ],
        'mstyle' : ['' , '' ],
        'msize'  : [ms , ms ],
    },
    'plot1'  : {
        'mode'   : ['line'],
        'label'  : ['Q'],
        'color'  : ['b'],
        'lstyle' : ['-'],
        'wstyle' : [ws ],
        'mstyle' : ['' ],
        'msize'  : [ms ],
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

    # Settings for surface temperature:
    't2m_plot' : {
        'plt_label'  : 'Surface temperature',          # plot title,
        'y_label'    : 'Temperature, deg C',           # y axis label
        'ylimits'    : [-30.0, 30.1, 10.0],            # ymin, ymax, ystep values or time
    },
    # Settings for precipitations:
    'prec_plot' : {
        # Settings for labels:
        'plt_label'  : 'Precipitations',
        'y_label'    : 'Precipitations, mm',
        'ylimits'    : [0.0, 15.1, 5.0],
    },      
    # Settings for density:
    'q_plot' : {
        'plt_label'  : 'Snow dencity',
        'y_label'    : 'Snow dencity, kg m-3',
        'ylimits'    : [0.0, 1000.1, 200],
    },
}

# Additional user settings for plots:
name_plot = ['SWE, mm', 'SD, cm'] # Create a y axis name - need for understanding
leg_pos   = ['upper left','upper right'] # Create a legend position
#            SWE,    SD 
y_min  = [   0.0,   0.0 ]
y_max  = [ 250.1, 120.1,]
y_step = [  50.0,  25.0 ]

#=============================    Main program   ==============================
if __name__ == '__main__':
    # -- Create output folder
    pout = l4s.makefolder(pout)
    # -- Cleaning previous results:
    l4s.clean_history(pout)
    # -- Get initial data
    lst4sd = []       # SD data
    lst4swe = []      # SWE data
    lst4t2m_prec = [] # T2m, Prec data
    for station in lst4stations:
        # -- Input path
        pin_sd       = pin + f'/SD/{station}.txt'
        pin_swe      = pin + f'/SWE/{station}.txt'
        pin_t2m_prec = pin + f'/T2M-PREC/{station}.txt'

        # -- Read data
        lst4sd.append(l4p.get_meteo_ru_sd(pin_sd))
        lst4swe.append(l4p.get_meteo_ru_swe(pin_swe))
        lst4t2m_prec.append(l4p.get_meteo_ru_t2m_prec(pin_t2m_prec)) 

    # -- Create complex plot:
    for  tr in range(len(t1)):
        # Create a timestep labels for plot names    
        t1_out = str(t1[tr])[0:4] + str(t1[tr])[5:7] + str(t1[tr])[8:10]
        t2_out = str(t2[tr])[0:4] + str(t2[tr])[5:7] + str(t2[tr])[8:10]

        period = pd.date_range(t1[tr], t2[tr], freq = 'D')
        # Cycle by stations
        for j in range(len(lst4stations)):
            t2m_min  = lst4t2m_prec[j]['T2m_min'][period].resample(step).mean()
            t2m_mean = lst4t2m_prec[j]['T2m_mean'][period].resample(step).mean()
            t2m_max  = lst4t2m_prec[j]['T2m_max'][period].resample(step).mean()
            prec     = lst4t2m_prec[j]['Prec'][period].resample(step).mean()
            sd       = lst4sd[j]['SD'][period].resample(step).mean()
            swe      = lst4swe[j]['SWE'][period].resample(step).mean()
            q_water  = ((sd / 2) * (4 /3)) * 5 

            # -- Create a zero DataFrame for precipitation data:
            df_zero = pd.DataFrame(data = np.full((len(prec),2),-9999))
            # Create data timeseries for different type of precipitations:
            prec_liq = pd.Series(df_zero[0].values, index = prec.index, dtype = 'float')
            prec_sol = pd.Series(df_zero[1].values, index = prec.index, dtype = 'float')

            # -- Change values:
            for row in range(len(t2m_mean)):
                if t2m_mean[row] < 1.2:
                    prec_sol[row] = prec[row]
                    prec_liq[row] = np.nan
                else:
                    prec_sol[row] = np.nan
                    prec_liq[row] = prec[row]

            # Create plots
            fig = plt.figure(figsize = (14,10))
            # -- Задание координатной сетки и места где будут располагаться графики
            egrid = (4,4)
            ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
            ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
            ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
            # add subplot in plot ax3
            bx1 = ax3.twinx()      
            ax4 = plt.subplot2grid(egrid, (3,0), colspan = 4)
            #Работа с формой для комплексного графика
            rcParams['figure.subplot.left']   = 0.1  # Левая граница
            rcParams['figure.subplot.right']  = 0.95 # Правая граница
            rcParams['figure.subplot.bottom'] = 0.1  # Нижняя граница
            rcParams['figure.subplot.top']    = 0.95 # Верхняя граница
            rcParams['figure.subplot.hspace'] = 0.4  # Общая высота, выделенная для свободного пространства между subplots

            # Temperature plot:
            #name_station = river_names[num]
            #ax.set_title('River: ' + name_st + ' ( ' + 'Meteostation: ' + nst + ' )', color = 'black', fontsize = 14, pad = 20)
            l4v.create_plot(ax1, [t2m_max, t2m_mean, t2m_min], lst4plot_settings, 't2m_plot', 'plot3')

            # Precipitation plot:
            l4v.create_plot(ax2, [prec_sol, prec_liq], lst4plot_settings, 'prec_plot', 'plot2_bar')

            # Snow plot
            leg_1 = 'SWE'
            leg_2 = 'SD'
            num = 0
            snow = l4v.plot_ml_2(
                ax3, bx1,  swe,  sd, leg_1, leg_2, name_plot[num], name_plot[num + 1],
                y_min[num], y_max[num], y_step[num], y_min[num + 1], y_max[num + 1], y_step[num + 1],
                leg_pos[num]  , leg_pos[num + 1], t1[tr], t2[tr])

            # Q plot:
            l4v.create_plot(ax4, [q_water], lst4plot_settings, 'q_plot', 'plot1')

            # Save plot:
            plt.savefig(
                f'{pout}/Station_{lst4stations[j]}_{t1_out}_{t2_out}.png',
                format='png', dpi = 300)
            plt.close(fig)
            plt.gcf().clear()

    if lbox_plot is True:
        # A box plot
        param_list = ['T2m_max', 'T2m_mean', 'T2m_min', 'Prec']

        for j in range(len(lst4stations)):

            data = lst4t2m_prec[j]
            fig_bp = plt.figure(figsize = (14,10))
            ax_bp  = fig_bp.add_subplot(111)

            #data['month'] = t2m_prec_list[j]['T2m_min'].index.month
            data['month'] = data.index.month

            for var in param_list:
                ax_bp = data.boxplot(column = var, by = 'month')
                ax_bp.set_title(" ")
                labels = [item.get_text() for item in ax_bp.get_xticklabels()]
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                labels[:] = months
                ax_bp.set_xticklabels(labels);

                plt.savefig(
                    f'{pout}/Box_plot/Station_{lst4stations[j]}_{var}.png',
                    format = 'png', dpi = 300) 
# =============================    End of program   =======================
