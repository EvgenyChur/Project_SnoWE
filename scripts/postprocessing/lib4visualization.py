# -*- coding: utf-8 -*-
"""
Description: Module for visualization of ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    20.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter

# Additional parameters for X and Y axis for plots
#------------------------------------------------------------------------------
minorLocator   = AutoMinorLocator (n=5)
minorFormatter = FormatStrFormatter('%.1f')

years   = mdates.YearLocator() #every year
days    = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')


# Function plt_line --> START
def plt_line(ax, data, label:str, color:str, lstyle:str, lwidth:str):
    '''
    Task: Create linear plot

    Parameters
    ----------
    ax : Subplot
    data : Series
        Time series for research parameter
    label : Legend for parameter line
    color : Color for parameter line
    lstyle : Line style for parameter line
    lwidth : Line wight for parameter line

    Returns
    -------
    ax : Subplot
    '''
    ax.plot(
        data.index,
        data,
        label = label,
        color = color,
        ls    = lstyle, # ls  = linestyle
        lw    = lwidth, # lw  = linewidth
    )
    #return ax
# Function plt_line --> END


# Function plt_scatter --> START
def plt_scatter(ax, data, label:str, color:str, msize:str, mstyle:str):
    '''
    Task: Create scatter plot

    Parameters
    ----------
    ax : Subplot
    data : Series
        Time series for research parameter
    label : Legend for parameter
    color : Color for parameter
    msize : Marker style for parameter line
    mstyle : Marker wight for parameter line

    Returns
    -------
    ax : Subplot
    '''
    ax.scatter(
        data.index,
        data,
        label = label,
        color = color,
        s     = msize,
        marker= mstyle,
    )
    #return ax
# Function plt_scatter --> END

def plt_bar(ax, data, label:str, color:str):
    '''
    Task: Create bar plot

    Parameters
    ----------
    ax : Subplot
    data : Series
    label : Legend for parameter
    color : Color for parameter

    Returns
    -------
    ax : Subplot
    '''
    ax.plot(data.index, data, label = label, color = color)
    #return ax

# Function plot_settings --> START
def plot_settings(
    ax, set4plots:dict, plot_type:str, lplt_title = True, lx_label = False, ly_label = True,
    llegend = True, lsecond_yaxis = False):
    '''
    Task: Set user settings for creation a nice plot

    ax : AxesSubplot
    set4plots : User settings for plot
    plot_type : Plot type (SD, RHO, SWE)
    lplt_title : bool, Optional
        Do you want to add plot title?
    lx_label : bool, Optional
        Do you want to add x label?
    ly_label : bool, Optional
        Do you want to add y label?
    llegend : bool, Optional
        Do you want to add legend?
    lsecond_yaxis : bool, Optional
        Do you want to add second axis?

    Returns
    -------
    ax : AxesSubplot
    '''
    #-- User settings:
    #-- Plot labels:
    plt_label = set4plots.get(plot_type).get('plt_label')  # plot title
    x_label   = set4plots.get('x_label')                   # x axis label
    y_label   = set4plots.get(plot_type).get('y_label')    # y axis label
    leg_loc   = set4plots.get('l_location')                # legend location
    #-- X axis limits:
    xformat   = set4plots.get('xformat')[0]                # format of axis by x axis (TIME or VALUES)
    mj_xticks = set4plots.get('xformat')[1]                # In case of TIME format you have to
                                                           # select time format
    xmin      = set4plots.get('xlimits')[0]                # xmin values   or time
    xmax      = set4plots.get('xlimits')[1]                # xmax values   or time
    xstep     = set4plots.get('xlimits')[2]                # x step values or time step
    #-- In case of time units by X axis we can apply special time settings
    mi_xticks = days                                       # options: days, years
    #-- Y axis limits:
    ymin      = set4plots.get(plot_type).get('ylimits')[0] # ymin values
    ymax      = set4plots.get(plot_type).get('ylimits')[1] # ymax values
    ystep     = set4plots.get(plot_type).get('ylimits')[2] # y step
    #-- X and Y settings for numbers:
    rotation = set4plots.get('rotation')                   # rotation of numbers by X axis
    fsize    = set4plots.get('fsize')                      # size of numbers for X and Y axes
    #-- Label text settings:
    clr       = 'black'                                    # color of labels
    fsize     = 14.0                                       # labels size
    lpab      = 20.0                                       # pad between axis and labels
    #-- Grid settings:
    gr_clr    = 'grey'                                     # grid line color  (black, red, blue, ...)
    gr_style  = 'solid',                                   # grid line type   ('dashed', ...)
    gr_tran   = 0.2                                        # grid transparency (0 - 1)

    #-- Set plot title, x and y axes labels
    if lplt_title is True:
        ax.set_title(plt_label, color = clr, fontsize = fsize, pad      = lpab)
    if lx_label is True:
        ax.set_xlabel(x_label , color = clr, fontsize = fsize, labelpad = lpab)
    if ly_label is True:
        ax.set_ylabel(y_label , color = clr, fontsize = fsize, labelpad = lpab)

    #-- Set plot legend
    if llegend == True:
        # Option 1: Simple
        ax.legend(loc = leg_loc, frameon = False)

        # Option 2: Use special text settings for legend:
        #font = font_manager.FontProperties(
        #    family = 'Arial', style  = 'normal', size   = fsize)
        #ax.legend(loc = leg_pos, frameon = True, prop = font, bbox_to_anchor=(0.5, -0.05))

    #-- Get x ticks parameters
    if xformat == 'time':
        ax.set_xticks(pd.date_range(xmin, xmax, freq = xstep))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(mj_xticks))
        # If you want to add additional ticks for x axis - use below code line
        #ax.xaxis.set_minor_locator(mi_xticks)
    elif xformat == 'values':
        ax.set_xticks(np.arange(xmin, xmax, xstep))

    #-- Get y ticks parameters
    ax.set_yticks(np.arange(ymin, ymax, ystep))

    if lsecond_yaxis == True:
        ax.tick_params(
            axis = 'y' , which ='major', bottom = True  , top = False,
            left = True, right = True  , labelleft ='on', labelright = 'on'
        )
        ax.tick_params(
            axis = 'y' , which ='minor', bottom = True  , top = False,
            left = True, right = True  , labelleft ='on', labelright = 'on'
        )
    #-- Additional ticks settings
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_minor_formatter(NullFormatter())
    #-- Parameters for ticks:
    tick_rotation_size(ax, rotation, fsize)
    #-- Grid settings
    ax.grid(True, which='major', color=gr_clr, linestyle=gr_style, alpha=gr_tran)
    #return ax
# Function plot_settings --> END


# Function tick_rotation_size  --> START
def tick_rotation_size(ax, rotation:int, fsize:int):
    '''
    Task: Additional setting for x and y axis

    Parameters
    ----------
    ax : AxesSubplot
    rotation : rotation of x axis labels
    fsize : size of plot numbers

    Returns
    -------
    ax : AxesSubplot
    '''
    # Set size and position of x and y values (ticks)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(rotation)
        label.set_fontsize(fsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(fsize)

    #return ax
# Function tick_rotation_size  --> END

def create_plot(ax, lst4data:list, set4plots:dict, plot_type:str, nlines = None):
    '''
    # Task: Create plot for research parameter depending on data types

    Parameters
    ----------
    ax : Subplot
    lst4data :  Time series for the research parameters
    set4plots : Plot settings
    plot_type : Plot type (SD, RHO, SWE)
    nlines : Numbers of plot lines
    Returns
    -------
        Figure
    '''
    # -- User settings
    if nlines != None:
        mode     = set4plots.get(nlines).get('mode')   # plot type
        labels   = set4plots.get(nlines).get('label')  # Legend labels
        colors   = set4plots.get(nlines).get('color')  # line color
        ln_style = set4plots.get(nlines).get('lstyle') # line style
        ln_width = set4plots.get(nlines).get('wstyle') # line wight
        mr_style = set4plots.get(nlines).get('mstyle') # marker style
        mr_size  = set4plots.get(nlines).get('msize')  # marker size

    else:
        mode     = set4plots.get('mode')   # plot type
        labels   = set4plots.get('label')  # Legend labels
        colors   = set4plots.get('color')  # line color
        ln_style = set4plots.get('lstyle') # line style
        ln_width = set4plots.get('wstyle') # line wight
        mr_style = set4plots.get('mstyle') # marker style
        mr_size  = set4plots.get('msize')  # marker size

    #-- Create plots based on data:
    for i in range(len(lst4data)):
        if mode[i] == 'line':
            plt_line(
                    ax, lst4data[i], labels[i], colors[i], ln_style[i], ln_width[i])
        elif mode[i] == 'scatter':
            plt_scatter(
                    ax, lst4data[i], labels[i], colors[i], mr_size    , mr_style[i])
        elif mode[i] == 'bar':
            plt_bar(ax, lst4data[i], labels[i], colors[i])
        else:
            sys.exit('Error: Figure mode has inappropriate type.')

    #-- Apply function for plot axis settings:
    plot_settings(ax, set4plots, plot_type)



#------------------------------------------------------------------------------
# Subroutine: plot_ml_2
#------------------------------------------------------------------------------
#
# Функция для построения графиков с 2 переменными: in one plot
#
#
# Input parameters:   prr_1, prr_2     - the main parameters
#                     leg_1, leg_2     - the main labels
#                     nam_3, nam_4     - the name of y axis
#                     pr_2, pr_3, pr_4 - the asis y limits
#                                        (pr_2 - low limit,
#                                         pr_3 - upper limit,
#                                         pr_4 - step)
#                     pr_5, pr_6, pr_7 - the asis y limits
#                                        (pr_5 - low limit,
#                                         pr_6 - upper limit,
#                                         pr_7 - step)
#                     l_p_1            - the legend position
#                     l_p_2            - the legend position
#                     time_step_1      - the start date
#                     time_step_2      - the stop date
#
#
# Author: Evgenii Churiulin, Center for Environmental Systems
#                                         Research (CESR) --- 16.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def plot_ml_2(ax, bx, prr_1, prr_2, leg_1, leg_2,
                      nam_3, nam_4,
                      pr_2, pr_3, pr_4,
                      pr_5, pr_6, pr_7,
                      l_p_1, l_p_2,
                      time_step_1, time_step_2):
    # The axis y - 1
    ax.scatter(prr_1.index, prr_1, s = 50, label = leg_1, color = 'r')
    ax.set_ylabel(nam_3, color = 'red', fontsize = 14, labelpad = 35 )
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_2, pr_3, pr_4))
    ax.legend(loc = l_p_1, frameon=False)
    ax.get_xticks()
    xbxx = ax.xaxis
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(xftm)
#    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    xbxx.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    ax.grid(True  , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)

    # The axis y - 2
    bx.plot(prr_2.index, prr_2, label = leg_2, color = 'blue', linestyle = '-.')
    bx.set_ylabel(nam_4, color = 'blue', fontsize = 14)
    bx.get_yticks()
    bx.set_yticks(np.arange(pr_5, pr_6, pr_7))
    bx.legend(loc = l_p_2, frameon=False)
    bx.get_xticks()

# plot_ml_2
#------------------------------------------------------------------------------






