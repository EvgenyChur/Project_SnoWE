# -*- coding: utf-8 -*-
"""
Description: Module for work with time limits

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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_time_periods(ref_date1:str, ref_date2:str, n_periods:int, years2add:int):
    '''
    Task: Create time filter based on year dynamic
    '''
    time_format = '%Y-%m-%d'
    # -- Create time filter:
    print('Creating winter time filter for the research data')
    #-- Reference time steps (start first year, end first year )
    refer_step1 = datetime.strptime(ref_date1, time_format)
    refer_step2 = datetime.strptime(ref_date2, time_format)
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

    return periods

def get_time_periods4gif(ref_date:str, n_periods:int, days2add:int):
    '''
    Task: Create time filter based on days dynamic
    '''
    time_format = '%Y-%m-%d'

    print('Creating gif time filter for the research data')
    #-- Reference time step (constant on every step)
    refer_step = datetime.strptime(ref_date, time_format)
    #-- Actual time step (will change)
    act_step   = refer_step
    #-- Create time list:
    periods = []
    for i in range(n_periods):
        act_step = act_step + timedelta(days = days2add)
        periods.append([refer_step, act_step])
    return periods

def fixed_timestep():
    '''
    Task: Get timesteps for fixed snow survey measurements (field and forest)
    '''

    time_step = [
        '2013-10-10','2013-10-20','2013-10-31','2013-11-10','2013-11-20','2013-11-30',
        '2013-12-10','2013-12-20','2013-12-31','2014-01-10','2014-01-20','2014-01-31',
        '2014-02-10','2014-02-20','2014-02-28','2014-03-10','2014-03-20','2014-03-31',
        '2014-04-10','2014-04-20','2014-04-30','2014-05-10','2014-05-20','2014-05-31',
        '2014-10-10','2014-10-20','2014-10-31','2014-11-10','2014-11-20','2014-11-30',
        '2014-12-10','2014-12-20','2014-12-31','2015-01-10','2015-01-20','2015-01-31',
        '2015-02-10','2015-02-20','2015-02-28','2015-03-10','2015-03-20','2015-03-31',
        '2015-04-10','2015-04-20','2015-04-30','2015-05-10','2015-05-20','2015-05-31',
        '2015-10-10','2015-10-20','2015-10-31','2015-11-10','2015-11-20','2015-11-30',
        '2015-12-10','2015-12-20','2015-12-31','2016-01-10','2016-01-20','2016-01-31',
        '2016-02-10','2016-02-20','2016-02-29','2016-03-10','2016-03-20','2016-03-31',
        '2016-04-10','2016-04-20','2016-04-30','2016-05-10','2016-05-20','2016-05-31',
        '2016-10-10','2016-10-20','2016-10-31','2016-11-10','2016-11-20','2016-11-30',
        '2016-12-10','2016-12-20','2016-12-31','2017-01-10','2017-01-20','2017-01-31',
        '2017-02-10','2017-02-20','2017-02-28','2017-03-10','2017-03-20','2017-03-31',
        '2017-04-10','2017-04-20','2017-04-30','2017-05-10','2017-05-20','2017-05-31',
        '2017-10-10','2017-10-20','2017-10-31','2017-11-10','2017-11-20','2017-11-30',
        '2017-12-10','2017-12-20','2017-12-31','2018-01-10','2018-01-20','2018-01-31',
        '2018-02-10','2018-02-20','2018-02-28','2018-03-10','2018-03-20','2018-03-31',
        '2018-04-10','2018-04-20','2018-04-30','2018-05-10','2018-05-20','2018-05-31']
        # Add for more modern datasets:
        #'2018-10-10','2018-10-20','2018-10-31','2018-11-10','2018-11-20','2018-11-30',
        #'2018-12-09','2018-12-20','2018-12-31','2019-01-10','2019-01-20','2019-01-31',
        #'2019-02-10','2019-02-20','2019-02-28','2019-03-10','2019-03-20','2019-03-31',
        #'2019-04-10','2019-04-20','2019-04-30','2019-05-10','2019-05-20','2019-05-31']

    dtime = pd.to_datetime(time_step, format = '%Y-%m-%d')

    return dtime
