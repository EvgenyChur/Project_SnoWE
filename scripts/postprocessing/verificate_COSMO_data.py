# -*- coding: utf-8 -*-
"""
Description: Create verification plots based on COSMO, COSMO_HYBRYD and SYNOP data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    14.09.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    26.04.2023 Evgenii Churiulin, MPI-BGC
           Prepared new version
"""
# =============================     Import modules     ====================
# 1.1: Standard modules
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
# 1.2 Personal modules
import lib4system_suport as l4s
import lib4processing as l4p
import lib4visualization as l4v

# =============================   Personal functions   ====================
def create_time_index(df):
    year  = df.iloc[:,0]
    month = df.iloc[:,1]
    day   = df.iloc[:,2]
    t_index = [
        pd.to_datetime(f'{i}-{j}-{z}',
                       format = '%Y-%m-%d') for i,j,z, in zip(year, month, day)]
    return t_index

def create_ts(df, t_index, var):
    return pd.Series(df[var].values, index = t_index, name = var)

# ================   User settings (have to be adapted)  =================

main = 'D:/Churyulin/DVINA'
# Input paths:
pin_sypon  = main + '/meteo/result_2000_2019/'                                 # SYNOP
pin_cosmo  = main + '/result_general/data_series/original_COSMO/0-24/'         # COSMO
pin_hybrid = main + '/result_general/data_series/Hybrid/0-24/'                 # COSMO Hybrid

# Output path:
pout = main + '/result_general/verification_plot/'

# -- User settings for complex plot:
lst4plot_settings = {
    # Settings for T2m plot:
    't2m_plot':{
        'mode'       : ['line' , 'line'  , 'line'  ],
        'label'      : ['COSMO', 'OBS'   , 'HYBRID'],
        'color'      : ['blue' , 'orange', 'green' ],
        'lstyle'     : [  '-'  ,   '-.'  , '--'    ],
        'wstyle'     : [ 1.0   ,   1.0   ,  1.0    ],
        'mstyle'     : [  ''   ,   ''    , ''      ],
        'msize'      : [ 50.0  ,  50.0   , 50.0    ],
        'plt_label'  : 'Comparison of air temperature',
        'y_label'    : 'Temperature, deg',
        'ylimits'    : [-30.0, 30.1, 10],
    },
    # Settings for TD2m plot
    'td2m_plot':{
        'mode'       : ['line' , 'line'  , 'line'  ],
        'label'      : ['COSMO', 'OBS'   , 'HYBRID'],
        'color'      : ['blue' , 'orange', 'green' ],
        'lstyle'     : [  '-'  ,   '-.'  , '--'    ],
        'wstyle'     : [ 1.0   ,   1.0   ,  1.0    ],
        'mstyle'     : [  ''   ,   ''    , ''      ],
        'msize'      : [ 50.0  ,  50.0   , 50.0    ],
        'plt_label'  : 'Comparison of dew point',
        'y_label'    : 'Temperature, deg',
        'ylimits'    : [-30.0, 30.1, 10],
    },
    # Settings for precipitation plot
    'prec_plot':{
        'mode'       : ['line' , 'line'  , 'line'  ],
        'label'      : ['COSMO', 'OBS'   , 'HYBRID'],
        'color'      : ['blue' , 'orange', 'green' ],
        'lstyle'     : [  '-'  ,   '-.'  , '--'    ],
        'wstyle'     : [ 1.0   ,   1.0   ,  1.0    ],
        'mstyle'     : [  ''   ,   ''    , ''      ],
        'msize'      : [ 50.0  ,  50.0   , 50.0    ],
        'plt_label'  : 'Comparison of precipitations',
        'y_label'    : 'Precipitation, mm',
        'ylimits'    : [0.0, 30.1, 5.0],
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
}

#=============================    Main program   ==============================
if __name__ == '__main__':
    # Create output folder
    pout = l4s.makefolder(pout)
    
    # Cleaning previous results:
    l4s.clean_history(pout)

    # Start data processing:
    dirs_real = sorted(os.listdir(pin_sypon))

    for file in dirs_real:
        # Get SYNOP data:
        df_real = l4p.get_csv_data(pin_sypon + f'/{file}')
        # Get COSMO data:
        df_cosmo = l4p.get_csv_data(
            pin_cosmo + f'/data_{file}' , separ = ',', headers = 0)
        # Get COSMO HYBRID
        df_hybrid = pd.read_csv(
            pin_hybrid + f'/data_{file}', separ = ',', headers = 0)

        # Make corrections:
        df_real = df_real[np.isfinite(df_real['R24'])]

        # Create new time index for COSMO and COSMO HYBRID datasets:
        cosmo_index  = create_time_index(df_cosmo)
        hybrid_index = create_time_index(df_hybrid)

        # Data from COSMO oper:
        t_2m        = create_ts(df_cosmo, cosmo_index , 'T_2M'     )
        td_2m       = create_ts(df_cosmo, cosmo_index , 'TD_2M'    )
        relhum_2m   = create_ts(df_cosmo, cosmo_index , 'RELHUM_2M')
        qv_s        = create_ts(df_cosmo, cosmo_index , 'QV_S'     )
        tot_precip  = create_ts(df_cosmo, cosmo_index , 'TOT_PREC' )

        # Data from COSMO hybrid:
        t_2m_h      = create_ts(df_cosmo, hybrid_index, 'T_2M'     )
        td_2m_h     = create_ts(df_cosmo, hybrid_index, 'TD_2M'    )
        relhum_2m_h = create_ts(df_cosmo, hybrid_index, 'RELHUM_2M')
        qv_s_h      = create_ts(df_cosmo, hybrid_index, 'QV_S'     )
        tot_precip_h= create_ts(df_cosmo, hybrid_index, 'TOT_PREC' )

        # Visualization:
        fig = plt.figure(figsize = (14,10))

        #Задание координатной сетки и места где будут располагаться графики
        egrid = (3,4)
        ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
        ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
        ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)

        # Complex plot boundaries (left, right, bottom, top, space)
        rcParams['figure.subplot.left']   = 0.1
        rcParams['figure.subplot.right']  = 0.95
        rcParams['figure.subplot.bottom'] = 0.1
        rcParams['figure.subplot.top']    = 0.95
        rcParams['figure.subplot.hspace'] = 0.4

        # T2m plot (deg C)
        lst4data = [t_2m, df_real['t2m'],t_2m_h]
        l4v.create_plot(ax1, lst4data, lst4plot_settings, 't2m_plot')

        # TD2m plot (def С)
        lst4data = [td_2m, df_real['td2m'], td_2m_h]
        l4v.create_plot(ax2, lst4data, lst4plot_settings, 'td2m_plot')
        
        # Precipitation plot (mm)
        lst4data = [tot_precip, df_real['R24'], tot_precip_h]
        l4v.create_plot(ax2, lst4data, lst4plot_settings, 'prec_plot')

        # Save plot
        plt.savefig(f'{pout}/{file[0:5]}.png', format = 'png', dpi = 300)
        plt.gcf().clear()
#=============================    End of program   ============================
