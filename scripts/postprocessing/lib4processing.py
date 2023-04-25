# -*- coding: utf-8 -*-
"""
Description: Module for data processing

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
import pandas as pd

def get_csv_data(
    path:str, separ = ';', skiprow = 0, headers = 'infer',
    nan_values = ['9990','********']):

    '''
    Task: Get preprocessed data

    Parameters
    ----------
    path : Input path
    separ : str, Optional
        Text separator. The default is ';'.
    skiprow : int, Optional
        Skip rows. The default is 0.

    Returns : DataFrame with processed data
    '''
    return pd.read_csv(
        path,
        skiprows = skiprow,
        sep = separ,
        dayfirst = True,
        parse_dates = True,
        index_col = [0],
        header = headers,
        skipinitialspace = True,
        na_values= nan_values,
    )

def get_ecomag_data(path:str, sypot_stations:list, path_out:str):
    '''
    Task: Reading ECOMAG input data, renaming columns, filtering by station ID
          and saving filter data as a independent csv file

    Parameters
    ----------
    path_in : str --> Input path
    sypot_stations: list of SYNOP stations
    path_out : Output path

    Returns: None --> Create output files in output folder
    '''
    # Lacal parameters:
    out_header = 'swe'

    # Get data:
    df = get_csv_data(path, skiprow = 2)

    # List of meteorological station for research in ECOMAG model.

    # Potentially columns names can be presented as a list filled in manually
    #lst4ecomag_st = [
    #     601,  604,  612,  670,  672,  706,  708,  709,  713,  735,  737,  773,
    #     788,  806,  825,  827,  851,  884,  917,  929,  934,  966,  979,  990,
    #     997, 1021, 1029, 1047, 1093, 1103, 1105, 1164, 1172, 1179, 1227, 1235,
    #    1244, 1325, 1341, 1399, 1459, 1536,
    #]

    # or you can use command. !Recommendation: check ECOMAG station ID and
    # SYNOP IP before computations
    lst4ecomag_st = list(df.columns.values)


    # Fast quality control test:
    (print('Lists len is the same') if len(lst4ecomag_st) == len(sypot_stations)
                                     else sys.exit('Error: Lists are different')
                                     )
    # Rename columns
    for i in range(len(lst4ecomag_st)):
        df = df.rename(columns = {lst4ecomag_st[i]:sypot_stations[i]})

    # Select data by index and save them into files:
    for in_station in sypot_stations:
        df_out = df[str(in_station)]
        df_out.to_csv(
            path_out + str(in_station) +'.csv',
            sep = ';',
            float_format = '%.3f',
            header = [out_header],
        )

def get_obs_data(path_in:str, path_out:str):
    '''
    Task: Reading observation input data, renaming columns, filtering by type (field/forest)
          and saving filter data as a independent csv file

    Parameters
    ----------
    path_in : str --> Input path
    path_out : Output path

    Returns: None --> Create output files in output folder
    '''
    param = 'id_st'

    # Get data
    df = get_csv_data(path_in)

    # Преобразование и выгрузка информации для маршрутов в поле (лесу):
    for i in pd.Series(df[param].values).drop_duplicates():
        df_st = df.loc[df['id_st'] == i]
        df_st.to_csv(
            path_out + str(i) +'.csv', sep = ';', float_format = '%.3f')