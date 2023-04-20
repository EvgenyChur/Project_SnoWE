# -*- coding: utf-8 -*-
"""
Description: Create linear plots for SnoWE data

Authors: Evgenii Churiulin

Current Code Owner: Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    10.12.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    20.04.2023 Evgenii Churiulin, MPI-BGC
           Global updating of the script (v2.0)
"""

#=============================     Import modules     ======================
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from matplotlib import rcParams

# Personal modules:
import lib4visualization as l4v
#=============================   Personal functions   ======================
def get_data(ipath:str):
    # Read csv files
    return pd.read_csv(
        ipath, skiprows = 0, sep = ';', dayfirst = True, parse_dates = True, 
        index_col = [0], skipinitialspace = True, na_values = ['9990','********'],
    )

def create_table(df_model, df_fact, params:list, pout:str, fn_station:str):
    # local variables:
    merge_method = 'inner'
    # Create output table for the research parameter (model, in-situ):
    df_mod = df_model[params[0]]
    df_stat = df_fact[params[1]]
    # Merge data:
    df = pd.concat([df_mod, df_stat], axis = 1, join = merge_method)
    # Save merged dataframe:
    df.to_csv(
        pout + f'params[2]_{fn_station[0:5].csv}', sep=';', float_format='%.3f',
        header = ['model','in situ'], index_label = 'Index'
    )

#================   User settings (have to be adapted)  =======================

# Logical settings: 
lprep_data = False # Do you want to prepare snow data?
lmain_mode = True  # Do you want to start main calculations and get snow plots ? 
lprep_gif  = True  # Do you want to get snow data: 
                   #       1 - for Git plot (1 year)   (used for presentations) 
                   #       2 - for snow plots by years (main mode) 

# Paths settings:
main = 'D:/Churyulin/msu_cosmo/Moscow_data/Comparison'  # Common path for snow data:
if lprep_data is True:
    # Snow database (preprocessing step):
    #ds_snow = 'stations_ivan'
    ds_snow = 'field'
    
    # Input and output paths:
    pin  = main + f'/result_filter/{ds_snow}.csv'
    pout = main + '/in-situ'   
else:
    # Station ID. Data was prepared on the preprocessing step:
    ds_snow = '27417'
    # Input and output paths:
    pin_model = main + f'/data_snowe/{ds_snow}.csv'
    pin_situ  = main + f'/in-situ/{ds_snow}.csv'
    pout      = main   

# Settings for time filter:
if lprep_gif is not True:
    #  Select winter data:
    ref_date1 = '2006-09-01'
    ref_date2 = '2007-04-30'
    n_periods = 12
    years2add = 1
else:
    # Select data for GIF plot (snow in dynamics) - one year:
    n_periods = 46
    ref_date  = '2011-09-01'
    days2add  = 5
    
# Settings for plots:
lst4plot_settings = {
    # Common settings for plots: 
    'mode'       : 'mixed',                       # Plot type ('line', 'scatter' 'mixed')
    'label'      : ['Model', 'in-situ'],          # Legend labels
    'color'      : ['blue' , 'black'  ],          # line colors
    'lstyle'     : [  '-'  ,   '-'    ],          # line style   (if 'mode' = 'scatter' -> not active)
    'wstyle'     : [ 1.0   ,   1.0    ],          # line wight   (if 'mode' = 'scatter' -> not active)
    'mstyle'     : [  '^'  ,   'o'    ],          # marker style (if 'mode' = 'line'    -> not active)
    'msize'      : [ 50.0  ,  50.0    ],          # marker size  (if 'mode' = 'line'    -> not active)
    'l_location' : 'upper left',                  # legend location
    'x_label'    : 'X axis label was turned off', # x axis label (common for all. Was turned off)
    'xformat'    : ['time', '%Y-%m'],             # format of axis by x axis (time or values)
                                                  # available options:'%H', '%Y-%m-%d', '%Y' '%B' '%d-%m' %m-%d
    # ! xmin and xmax will be define later  !
    'xlimits'    : ['', '', '1M'],                # xmin, xmax, xstep values or time                                              
    'rotation'   : 0.0,                           # rotation of numbers by X axis (deg)
    'fsize'      : 14.0,                          # size of numbers for X and Y axes
    # Settings for snow depth plot:     
    'sd_plot' : {
        'plt_label'  : 'Snow depth',              # plot title,
        'y_label'    : 'Snow depth, s m-1',       # y axis label
        'ylimits'    : [0.0, 61.1, 15],           # ymin, ymax, ystep values or time
    },
    # Settings for snow density plot:
    'rho_plot' : {
        'plt_label'  : 'Snow density',
        'y_label'    : 'Snow density, g sm-3',
        'ylimits'    : [0.0, 1.01, 0.25],
    },
    # Settings for snow density plot:
    'swe_plot' : {
        # Settings for labels:
        'plt_label'  : 'Snow water equivalent',
        'y_label'    : 'Snow water equivalent, mm',
        'ylimits'    : [0.0, 151.1, 15.0],
    },  
} 
    
kg2g = 1000.0 # convert kg to gramm
#=============================    Main program   ==============================
if __name__ == '__main__': 
    # Data preprocessing. Select data for stations from and save the as 
    # separete .csv files:
    if lprep_data is  True:
        print ('Start data preprocessing:')
        # Get data from common snow dataset:
        df = (
            pd.read_csv(pin, sep = ';')
              .drop_duplicates()
              .set_index(['id_st'])
        )
        # Get stations ID from common snow dataset:
        stations = (
            get_data(pin)
                .iloc[:,0]
                .sort_values()
                .drop_duplicates()
        )
        # Select data by stations id and save data to the new csv files: 
        for st_index in stations:   
            # -- Select data for station:
            df_station = (
                df.filter(like = str(st_index), axis = 0)
                  .reset_index()
            )
            #-- Merge data:
            data_result = pd.concat(
                [pd.to_datetime(df_station.iloc[:,1]),
                 df_station.iloc[:,0], 
                 df_station.iloc[:,2], 
                 df_station.iloc[:,3],
                 df_station.iloc[:,4],
                 df_station.iloc[:,5],
                ], axis = 1
            )
            #-- Rename columns and set index:
            data_result.columns = ['date','id_st','route','sd','rho','swe']
            data_result = data_result.set_index(['date'])
            #-- Save files:
            data_result.to_csv(
                f'{pout}/{st_index}.csv', sep=';', float_format='%.3f', 
                index_label = 'date'
            )
    else:
        print('Data had been prepared early')
        
    # Main data processing part
    if lmain_mode is True:
        print('Main calculations:')    
        # -- Get model and in-situ data: 
        df_snowe = get_data(pin_model)
        df_situ  = get_data(pin_situ)
        
        # -- Create csv merge tables for the research parameters:
        #    p.s.: no data for in-situ stations (27515 - 2006, 2007 years
        #                                        27627 - 2006, 2008 years)
        create_table(df_snowe, df_situ, ['depth', 'sd' , 'sd_' ], pout, ds_snow)
        create_table(df_snowe, df_situ, ['rho'  , 'rho', 'rho_'], pout, ds_snow)
        create_table(df_snowe, df_situ, ['swe'  , 'swe', 'swe_'], pout, ds_snow)
        
        # -- Create time filter:
        if lprep_gif is not True:
            print('Creating winter time filter for the research data')
            #-- Reference time steps (start first year, end first year )
            refer_step1 = datetime.strptime(ref_date1, '%Y-%m-%d')
            refer_step2 = datetime.strptime(ref_date2, '%Y-%m-%d')
            #-- Actual time step (will change)
            act_step1 = refer_step1
            act_step2 = refer_step2
            #-- Create time list:
            periods = []
            for i in range(n_periods):
                if i == 0:
                    periods.append([refer_step1, refer_step2])
                else:
                    act_step1 = act_step1 + relativedelta(years = years2add)
                    act_step2 = act_step2 + relativedelta(years = years2add)
                    periods.append([act_step1, act_step2])
        else:
            print('Creating gif time filter for the research data')
            #-- Reference time step (constant on every step)
            refer_step = datetime.strptime(ref_date, '%Y-%m-%d')
            #-- Actual time step (will change)
            act_step   = refer_step
            #-- Create time list:
            periods = []
            for i in range(n_periods):
                act_step = act_step + timedelta(days = days2add)
                periods.append([refer_step, act_step])
        
        #-- Select data in actual time range
        for i in range(n_periods):
            # -- Select time range (t1 - start; t2 - stop)
            t1 = periods[i][0]
            t2 = periods[i][1]
            
            # -- Define time settings for x axis
            if lprep_gif is not True:
                lst4plot_settings.get('xlimits')[0] = t1 # xmin
                lst4plot_settings.get('xlimits')[1] = t2 # xmax
            else:
                lst4plot_settings.get('xlimits')[0] = periods[0][0]  # xmin
                lst4plot_settings.get('xlimits')[1] = periods[-1][1] # xmax            
       
            # -- Create plots:
            fig = plt.figure(figsize = (14,10))
            # -- Settings for plot with subplots
            # -- left, right, bottom, top borders hspace between subplots
            rcParams['figure.subplot.left']   = 0.1
            rcParams['figure.subplot.right']  = 0.95
            rcParams['figure.subplot.bottom'] = 0.1
            rcParams['figure.subplot.top']    = 0.95
            rcParams['figure.subplot.hspace'] = 0.4
               
            # -- Setting the coordinate grid and the place where the graphs will be located
            egrid = (3,4)
            ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
            ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
            ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
            
            # -- Create plots (SD, RHO, SWE):
            l4v.create_plot(
                ax1,
                #           model                in-situ 
                [df_snowe['depth'][t1:t2], df_situ['sd'][t1:t2]], 
                lst4plot_settings, 
                'sd_plot' )
            
            l4v.create_plot(
                ax2,
                #             model                  in-situ
                [df_snowe['rho'][t1:t2] / kg2g, df_situ['rho'][t1:t2]],
                lst4plot_settings,
                'rho_plot'
            )
            
            l4v.create_plot(
                ax3,
                #           model                in-situ
                [df_snowe['swe'][t1:t2], df_situ['swe'][t1:t2]],
                lst4plot_settings,
                'swe_plot',
            )
              
            # -- Save plot:
            t1_out = str(t1)[0:11]
            t2_out = str(t2)[0:11]
            
            output_plot = f'{pout}/plot_{ds_snow[0:5]}_{t1_out}_{t2_out}.png'
            plt.savefig(output_plot, format = 'png', dpi = 300) 
            plt.gcf().clear()
#=============================    End of program   ============================ 
 