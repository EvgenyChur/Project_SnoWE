# -*- coding: utf-8 -*-
"""
Description: Script for data processing of COSMO data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    19.03.2018 Evgenii Churiulin, RHMS
           Initial release
    1.2    26.04.2023 Evgenii Churiulin, MPI-BGC
           Prepared v2.0
"""
# =============================     Import modules     =====================
# 1.1: Standard modules
import os
import pandas as pd
import numpy  as np
# 1.2 Personal module
import lib4system_suport as l4s

# =============================   Personal functions   ====================
# Support function: Get metainformation about grid points!
def get_meta_data():
    # Task:Load excel file with additional metainformation about grid points
    df = pd.read_excel('D:/Churyulin/msu_cosmo/forecast/Meta.xlsx')
    # -- Select data from EXCEL meta file:
    df_refer = pd.concat([df.iloc[:,5], df.iloc[:,6], df.iloc[:,0]], axis = 1)
    # Rename columns:
    df_refer.columns = ['GPI','GPJ','ID_station']
    return df_refer
# end function

# Support function: Create new time index based on columns from Dataframe:
def create_time_index(df):
    year  = df.iloc[:,0]
    month = df.iloc[:,1]
    day   = df.iloc[:,2]
    hour  = df.iloc[:,3]
    # Create new time index
    t_index = [
        pd.to_datetime('{i}-{j}-{z}-{k}',
                       format='%Y-%m-%d-%H') for i,j,z,k in zip(year, month, day, hour)]
    return t_index
# end function

# Support function for reading COSMO data in txt format:
def get_cosmo_txt(pin:str):
    widths = [3, 1, 3, 1, 6, 1, 6, 1, 7, 1, 7, 1, 6, 1, 5, 1, 7]
    return pd.read_fwf(
        pin,
        widths = widths,
        skiprows = 0,
        skip_footer = 0,
        header = 0,
        )

# Reading COSMO data and groupby them by GPI and GPJ (Section 1)
def get_mean_GPI_GPJ_data(iPath:str, fileName:str, outPath:str):
    # Local variables:
    pout = f'{outPath}data_{fileName[4:12]}.txt'
    # Parameters for research:
    params = ['GPI','GPJ','RLON','RLAT','T_2M','TD_2M','RELHUM_2M','QV_S']

    # Open txt file with COSMO data:
    widths = [6,2,2,2,2, 8, 4, 6, 12, 12, 11, 12, 12, 12]
    df = pd.read_fwf(
        iPath, widths = widths, skiprows = 8, skip_footer = 0, header = 0)
    # Rename columns:
    df.columns = [
        'YYYY', 'MM', 'DD', 'HH','mm','LEVEL','GPI','GPJ','RLON','RLAT',
        'T_2M','TD_2M','RELHUM_2M','QV_S']

    # Create new index for data:
    cosmo_index = create_time_index(df)

    # Select data from dataframe by parameters and set new time index:
    lst4series = []
    for var in params:
        lst4series.append(pd.Series(df[var].values, index = cosmo_index))
    df_cosmo = pd.concat(lst4series, axis = 1)
    df_cosmo.columns = params

    # -- Groupby data by GPI and GPJ
    df_cosmo_group = df_cosmo.groupby(['GPI','GPJ'], as_index = False).mean()
    # -- Save prepared file:
    df_cosmo_group.to_csv(pout, sep = ',', float_format = '%.3f')
    print ('calculated: ' + fileName[4:12])

# Reading COSMO data with precipitations:
def get_cosmo_precipitation(iPath:str, fileName:str, outPath:str):
    # -- Local variables:
    # Output path for prepared data:
    pout = f'{outPath}data_{fileName[5:13]}.csv'
    # Indexes of the research parameters:
    params = [0,2,4,6,8,10,12,14,16]
    # Names of the research parameters:
    params_names = [
        'GPI','GPJ','RLON','RLAT','T_2M','TD_2M','RELHUM_2M','QV_S','TOT_PREC']

    # -- Load COSMO data:
    df = get_cosmo_txt(iPath)
    # -- Select data from dataframe by parameters:
    lst4series = []
    for var in params:
        lst4series.append(df.iloc[:,var])
    df_cosmo = pd.concat(lst4series, axis = 1)
    df_cosmo.columns = params_names

    # -- Load metadata for grid points:
    df_meta = get_meta_data()

    # -- Merge 2 dataframes:
    result = pd.merge(
        df_meta, df_cosmo, on = ['GPI','GPJ'], suffixes = ['_l', '_r'])

    # -- Save processed data:
    result.to_csv(pout, float_format = '%.3f', index = False)
    print (f'calculated: {fileName[5:13]}')
    return result

# Get COSMO data for meteorological station:
def get_cosmo_precipitation_maket(data_csv:list, path_in:str, path_exit:str):
    # Create array
    maket_data = ''
    for file in data_csv:
        df_temp = pd.read_csv(path_in + file, sep = ',', header = 0)
        if len(maket_data)> 0:
            maket_data = pd.concat([maket_data, df_temp])
        else:
            maket_data = df_temp
        print ('Идет сортировка данных:')

    # Data sorting
    for i in maket_data['ID_station']:
        result_data = (
            maket_data[maket_data['ID_station'].isin([i])]
                .drop(['ID_station'], axis = 1)
                .replace(np.nan, 0)
        )
        result_data.to_csv(
            path_exit + 'data_' + str(i) +'.csv',
            float_format = '%.3f', index = False)

# Get COSMO data for stations with precipitations:
def cosmo_model(data_csv:list, path_in:str, path_exit:str):
    # -- Local variables:
    # Indexes of the research parameters:
    params = [0,2,4,6,8,10,12,14,16]
    # Names of the research parameters:
    params_names = [
        'GPI', 'GPJ', 'RLON', 'RLAT', 'T_2M', 'TD_2M', 'RELHUM_2M', 'QV_S',
        'TOT_PREC' ]

    # -- Load metadata for grid points:
    df_meta = get_meta_data()

    #Объявление и назначение массива
    maket_data = ''
    for file in data_csv:
        df_temp = get_cosmo_txt(path_in + file)
        if len(maket_data) > 0:
            maket_data = pd.concat([maket_data, df_temp])
        else:
            maket_data = df_temp
        print ('Calculated:')

    # -- Select data from dataframe by parameters:
    lst4series = []
    for var in params:
        lst4series.append(maket_data.iloc[:,var])
    df_cosmo = pd.concat(lst4series, axis = 1)
    df_cosmo.columns = params_names

    # -- Merge data:
    result = pd.merge(df_cosmo, df_meta, on=['GPI','GPJ'], suffixes=['_l', '_r'])

    #Сортировка данных
    for i in result['ID_station']:
        result_data = (
            result[result['ID_station'].isin([i])]
                .drop(['ID_station'], axis = 1)
                .replace(np.nan, 0)
        )
        #  Save output file:
        result_data.to_csv(
            f'{path_exit}data_{i}.csv', float_format = '%.3f', index = False)
    return result

# ================   User settings (have to be adapted)  ==================
lprep_calc = True            # Do you want to run preprocessing of COSMO data (True / False)
lyear = False                # Do you use yerly data (archive) or quasi operational data (True / False)
lprep_precipitations = True  # Do you want to run preprocessing of COSMO data with precipitations? (True / False)
lcalc4stations = True        # Do you want to get COSMO data for stations?
lcalc4prec = False           # Do you want to additional data processing?

#=============================    Main program   ==============================
if __name__ == '__main__':
    # Preprocessing COSMO data.
    if lprep_calc is True:
        # Yearly data
        if lyear is True:
            # Section 1: Get mean values of COSMO parameters by GPI and GPJ
            main = 'C:/Python_script/msu_cosmo'
            years = [2012, 2013, 2014, 2015, 2016]
            for yr in years:
                # Temporal input and output paths:
                pin  = f'{main}/{yr}/'
                pout = f'{main}/results/{yr}/'
                # Data preprocessing (Get, Read and save to the new .csv file)
                for file in os.listdir(f'{pin}/'):
                    df = get_mean_GPI_GPJ_data(f'{pin}/file', pin, pout)

        # Data from time periods (0 - 72 hours)
        else:
            # Section 1: Get mean values of COSMO parameters by GPI and GPJ
            main = 'D:/Churyulin/msu_cosmo/forecast'
            cosmo_folders = ['0-24', '24-48', '48-72']
            for folder in cosmo_folders:
                # Input and output folders:
                pin = main + f'/{folder}/'
                pout = main + f'/result_oper/{folder}/'
                # Data preprocessing (Get, Read and save to the new .csv file)
                for file in os.listdir(f'{pin}/'):
                    df = get_mean_GPI_GPJ_data(f'{pin}/file', pin, pout)

    # Preprocessing COSMO precipitation data
    if lprep_precipitations is True:
        # -- Section 3: Preprocessing of COSMO presipitation data
        main = 'D:/Churyulin/msu_cosmo/forecast'
        cosmo_folders = ['0-24', '24-48', '48-72']
        cosmo_outputs = ['0 - 24', '24 - 48', '48 - 72']
        for i in range(len(cosmo_folders)):
            # Input and output folders:
            pin = main + f'/achive/result_archive/{cosmo_folders[i]}'
            pout = main + f'/presipitation/{cosmo_outputs[i]}/'
            # Make output folders and cleaning previous results:
            pout = l4s.makefolder(pout)
            l4s.clean_history(pout)
            # Data preprocessing (Get, Read and save to the new .csv file)
            for file in os.listdir(f'{pin}/'):
                df = get_cosmo_precipitation(f'{pin}/file', file, pout)

    if lcalc4stations is True:
        # -- Section 3, Step 2 --> Further work with COSMO presipitation
        main = 'D:/Churyulin/msu_cosmo/forecast/presipitation'
        cosmo_folders = ['0 - 24', '24 - 48', '48 - 72']
        for folder in cosmo_folders:
            # Input and output folders:
            pin = main + f'/{folder}/'
            pout = main + f'/final_result_station/{folder}/'
            # Make output folders and cleaning previous results:
            pout = l4s.makefolder(pout)
            l4s.clean_history(pout)
            # Run data processing (Sorting data by meteostations):
            df = get_cosmo_precipitation_maket(os.listdir(f'{pin}/'), pin, pout)

    if lcalc4prec is True:
        # -- Section 4. Create COSMO makets for stations with precipitations
        main = 'C:/Python_script/msu_cosmo/forecast'
        cosmo_folders = ['0 - 24', '24 - 48', '48 - 72']
        cosmo_outputs = ['0 - 24 result','24 - 48 result','48 - 72 result']
        for folder in range(len(cosmo_folders)):
            # Input and output folders:
            pin  = main + f'/result/{cosmo_folders[i]}/'
            pout = main + f'/result/{cosmo_outputs[i]}/'
            # Make output folders and cleaning previous results:
            pout = l4s.makefolder(pout)
            l4s.clean_history(pout)
            # Run data processing (Sorting data by meteostations):
            df = cosmo_model(os.listdir(pin), pin, pout)
