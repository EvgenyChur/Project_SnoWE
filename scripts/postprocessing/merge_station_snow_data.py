# -*- coding: utf-8 -*-
"""
Description: Программа для работы с метеорологическими данными, полученными из
             SYNOP кода с помощью скрипта (все данные в 1 файле) на tornado
             Программа осуществляет расчет среднесуточных значений
             метеорологических параметров

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    20.08.2018 Evgenii Churiulin, RHMS
           Initial release
    1.1    20.04.2023 Evgenii Churiulin, MPI-BGC
           Deep modernization
"""
# =============================     Import modules     ======================
# 1.1: Standard modules
import os
import numpy as np
import pandas as pd

# 1.2 Personal module
import lib4system_suport as l4s
import lib4processing as l4p

# =============================   Personal functions   ======================

# ================   User settings (have to be adapted)  ====================
# Logical settings:
lprep_calc = True # Do you want to run preprocessing? (True / False)
                  # Otherwise you can combine data in one dataset

# Select data paths:
mode = 'dvina'

# Common path for all data:
main = 'D:/Churyulin'

if lprep_calc is True:
    # Catalog of input paths:
    pin_catalog = {
        'moscow'   : main + '/msu_cosmo/Moscow_data/2000 - 2010/',
        'precip'   : main + '/snow data(ivan)/precipitation/',
        '4snowe'   : main + '/snow data(ivan)/inna_meteo_real/',
        'ivan_data': main + '/Ivan/data/',                                      # путь к данным по запросу студента Вани
        'inna_data': main + '/msu_cosmo/forecast/meteorological_data_oper/',    # путь к данным по запросу Инны Николаевны для Северной Двины
        'dvina'    : main + '/DVINA/2011-2019/',
        'don'      : main + '/DON/meteo_2000_2010/',
    }
    # Catalog of output paths:
    pout_catalog = {
        'don_data' : main + '/msu_cosmo/Data_Natalia_Leonidovna/Result_2000_2010/',
        'moscow'   : main + '/msu_cosmo/Moscow_data/result_2000_2010/',
        'precip'   : main + '/snow data(ivan)/result_data/',
        '4snowe'   : main + '/snow data(ivan)/inna_meteo_1day/',
        'ivan_data': main + '/Ivan/result/',                                    # путь к данным по запросу студента Вани
        'inna_data': main + '/msu_cosmo/forecast/in_situ_oper/',                # путь к данным по запросу Инны Николаевны для Северной Двины
        'dvina'    : main + '/DVINA/result_2011_2019',
        'don'      : main + '/DON/result_2000_2010/',
    }

    # Get actual input and output paths:
    pin = pin_catalog.get(mode)
    pout = pout_catalog.get(mode)

# -- You combine data from preprocessing step into 1 new output table
else:
    # Get actual input and output paths:
    pin1 = 'D:/Churyulin/DON/result_2000_2010/'
    pin2 = 'D:/Churyulin/DON/result_2011_2019/'
    pout = 'D:/Churyulin/DON/final'

# List of parameters for research:
params = [
        'date', 'index', 'lat'  , 'lon'   , 'height', 'ps'   , 'pmsl', 't2m',
        'td2m', 'dd10m', 'ff10m', 'tmin2m', 'tmax2m', 'tming', 'R12' , 'R24',
        't_g' , 'hsnow',
    ]

# Frequency for resampling
freq = '1D' # '1M'

# =============================    Main program   ==========================
if __name__ == '__main__':
    if lprep_calc is True:
        # Create output folder:
        pout = l4s.makefolder(pout)

        # Cleaning previous results:
        l4s.clean_history(pout)
    
        # Start preprocessing:
        for file in sorted(os.listdir(pin)):
            # -- Get data:
            df = (l4p.get_csv_data(f'{pin}{file}',
                                   headers = None,
                                   nan_values = ['******','********'])
                     .drop_duplicates(keep = False)
                     # Delete columns with unuseful information
                     .drop([ 5,  6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                            23, 24, 28, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                            42, 43, 44, 45, 46], axis = 1)
            )

            # -- Rename columns:
            # df.columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17] --> old version
            for i in range(len(list(df.columns.values))):
                df = df.rename(columns = {list(df.columns.values)[i]:params[i]})
            print ('Columns:'), df.columns

            # -- Change data type for column and use it as index
            df['date'] = pd.to_datetime(df['date'])
            df = df.reset_index(drop=True).set_index('date')

            # -- Make data corrections:
            for var in params[1:]:
                if var == 'ff10m':
                    df['ff10mean'] = df[var].resample(freq).mean()
                    df['ff10max']  = df[var].resample(freq).max()
                elif var in ['R12', 'R24']:
                      df[var][df[var] == 9990.0 ] = np.nan
                      if freq != '1D':
                          df[var] = df[var].resample(freq).sum()
                      else:
                          df[var] = df[var].resample(freq).mean()
                else:
                    df[var] = df[var].resample(freq).mean()

            # -- Delete field:
            df = df.drop(['ff10m'], axis = 1)

            # -- Save new dataframe
            df.to_csv(
                f'{pout}/{file[0:5]}.csv', sep=';', float_format='%.3f',
                index_label = 'Date')
    else:
        # Get sorted lists of preprocessed data:
        dirs1 = sorted(os.listdir(pin1))
        dirs2 = sorted(os.listdir(pin2))

        # Create output folder:
        pout = l4s.makefolder(pout)
        # Cleaning previous results:
        l4s.clean_history(pout)

        if len(dirs1) == len(dirs2):
            for file in sorted(os.listdir(dirs1)):
                df1 = l4p.get_csv_data(f'{pin1}{file}', nan_values = ['******','********'])
                df2 = l4p.get_csv_data(f'{pin2}{file}', nan_values = ['******','********'])

                # Concat data
                df_data = pd.concat([df1, df2])

                # -- Save output file:
                df_data.to_csv(
                    f'{pout}/{file}.csv', sep=';', float_format='%.3f',
                    index_label = 'Date'
                )
# =============================    End of program   ========================
