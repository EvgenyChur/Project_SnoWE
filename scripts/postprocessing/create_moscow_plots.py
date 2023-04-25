# -*- coding: utf-8 -*-
"""
Description: Программа предназначена для одновременной отрисовке данных о
             снежном покрове в Москве и Москвском регионе

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    31.10.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    25.04.2023 Evgenii Churiulin, MPI-BGC
           Prepared new version of the previous script
"""
# =============================     Import modules     =====================
# 1.1: Standard modules
import matplotlib.pyplot as plt

# 1.2 Personal module
import lib4visualization as l4v
import lib4system_suport as l4s
import lib4processing    as l4p
import lib4time_periods  as l4tp

# =============================   Personal functions   =====================

# ================   User settings (have to be adapted)  ===================
# Input data:
pin = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/data'

# Input stations:
lst4stations = [
    '27417', '27419', '27502', '27509', '27511', '27515', '27523', '27538',
    '27605', '27611', '27612', '27618', '27619', '27625', '27627', '557375']

nlines = 'plot16' # plot11

# Output paths:
pout = 'D:/Churyulin/msu_cosmo/Moscow_data/SWE/result/plot_1'

# -- Settings for time filter
ref_date1 = '2000-10-01'
ref_date2 = '2001-04-30'
n_periods = 18
years2add = 1

# -- Settings for plot:
ws = 1  # line wight
ms = 50 # marker size

lst4plot_settings = {
    # Uniq settings for plot with 16 lines:
    'plot16' : {
        # Plot type ('line', 'scatter', 'bar')
        'mode' : ['line'] * 16,
        # Labels for legend:
        'label' : [''] * 16,
        # line colors
        'color'  : ['blue'   , 'orange' , 'green'     , 'red' , 'purple', 'brown' ,
                    'pink'   , 'gray'   , 'olive'     , 'cyan', 'brown' , 'maroon',
                    'magenta','lavender', 'lightgreen', 'lime', 'salmon',         ],
        # line style   (if 'mode' = 'scatter' -> not active)
        'lstyle' : ['-' , '--', '-.', ':' , '-.', '--',
                    '-' , '--', '-.', ':' , '-.', '--',
                    '--', '-' , '--', '-.', ':'       ],
        'wstyle' : [ws] * 16, # line wight   (if 'mode' = 'scatter' -> not active)
        'mstyle' : [''] * 16, # marker style (if 'mode' = 'line'    -> not active)
        'msize'  : [ms] * 16, # marker size  (if 'mode' = 'line'    -> not active)
    },
    # Uniq settings for plot with 11 lines:
    'plot11' : {
        # Plot type ('line', 'scatter', 'bar')
        'mode'   : ['line'] * 11,
        'label'  : ['SnoWE'] * 11,
        'color'  : ['blue', 'orange', 'green', 'red' , 'purple', 'brown',
                    'pink', 'gray'  , 'olive', 'cyan', 'brown' ,        ],
        'lstyle' : ['-' , '--', '-.', ':' , '-.', '--',
                    '-' , '--', '-.', ':' , '-.',     ],
        'wstyle' : [ws] * 11,
        'mstyle' : [''] * 11,
        'msize'  : [ms] * 11,
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
    'sd_plot' : {'plt_label'  : 'Высота снега',
                 'y_label'    : 'Высота снега, sm',
                 'ylimits'    : [ 0.0, 80.1, 10.0],
    },
    # Settings for RHO plot:
    'rho_plot' : {'plt_label' : 'Плотность снега',
                  'y_label'   : 'Плотность снега, кг/м3',
                  'ylimits'   : [0.0, 700.1, 100.0],
    },
    # Settings for SWE plot:
    'swe_plot' : {'plt_label' : 'Запас воды в снеге',
                  'y_label'   : 'Запас воды в снеге, мм',
                  'ylimits'   : [0.0, 250.1, 25.0],
    },
}

#=============================    Main program   ==============================
if __name__ == '__main__':
    # -- Create output folder:
    pout = l4s.makefolder(pout)
    # -- Clean output folder:
    l4s.clean_history(pout)

    # -- Get data:
    lst4data = []
    for st_index in lst4stations:
        lst4data.append(l4p.get_csv_data(f'{pin}/{st_index}.csv'))

    # -- Get time periods:
    periods = l4tp.get_time_periods(ref_date1, ref_date2, n_periods, years2add)

    # -- Select data for plot and create it:
    for t in range(n_periods):
        # -- Select time range (t1 - start; t2 - stop)
        t1 = periods[t][0]
        t2 = periods[t][1]

        # -- Define several user settings for plots:
        # Labels for lines:
        if len(lst4stations) == len(lst4plot_settings.get(nlines).get('label')):
            for i in range(len(lst4stations)):
                lst4plot_settings.get(nlines).get('label')[i] = lst4stations[i]

        # Time settings for x axis
        lst4plot_settings.get('xlimits')[0] = t1 # xmin
        lst4plot_settings.get('xlimits')[1] = t2 # xmax

        # -- Define plot time prefix for output name:
        t1_out = str(t1)[0:11]
        t2_out = str(t2)[0:11]

        # -- Create lists for data:
        sd_data = []
        rho_data = []
        swe_data = []

        #-- Apply time filter for data:
        for i in range(len(lst4data)):
            sd_data.append(lst4data[i]['depth'][t1:t2])
            rho_data.append(lst4data[i]['rho'][t1:t2])
            swe_data.append(lst4data[i]['swe'][t1:t2])

        #-- Create plots:
        # Snow depth:
        fig = plt.figure(figsize = (14,10))
        ax = fig.add_subplot(111)
        l4v.create_plot(ax, sd_data, lst4plot_settings, 'plot_sd', nlines)
        plt.savefig(f'{pout}/SD_{t1_out}_{t2_out}.png', format = 'png', dpi = 300)
        plt.gcf().clear()

        # Snow density:
        fig2 = plt.figure(figsize = (14,10))
        bx   = fig2.add_subplot(111)
        l4v.create_plot(bx, rho_data, lst4plot_settings, 'plot_rho', nlines)
        plt.savefig(f'{pout}/RHO_{t1_out}_{t2_out}.png', format = 'png', dpi = 300)
        plt.gcf().clear()

        # Snow water equivalent:
        fig3 = plt.figure(figsize = (14,10))
        cx   = fig3.add_subplot(111)
        l4v.create_plot(cx, swe_data, lst4plot_settings, 'plot_swe', nlines)
        plt.savefig(f'{pout}/SWE_{t1_out}_{t2_out}.png', format='png', dpi = 300)
        plt.gcf().clear()
#=============================    End of program   ============================
