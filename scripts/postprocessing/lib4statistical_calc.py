# -*- coding: utf-8 -*-
"""
Description: Module for statistical computations

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    24.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""
import math
import pandas as pd

# Function 1 --> calc_MAE
def calc_MAE(ts):
    '''
    Task: Calculating MAE (Mean absolute error)

    Parameters
    ----------
    ts : Series
        Research parameter values.

    Returns
    -------
    mae_stat : float
        MAE.
    '''
    try:
        mae_stat = (sum(abs(ts))) / len(ts)
    except ZeroDivisionError:
        mae_stat = 0
    return mae_stat
# End of function!


# Function 2 --> calc_RMSE
def calc_RMSE(ts):
    '''
    Task: Calculating RMSE (Root measn squere error)

    Parameters
    ----------
    ts : Series
        Research parameter values.

    Returns
    -------
    rmse_stat : float
        RMSE
    '''
    try:
        rmse_stat = math.sqrt(sum(ts * ts) / len(ts))
    except ZeroDivisionError:
        rmse_stat = 0
    return rmse_stat
# End of function!


# Function 3 --> cacl_MAE_profit
def cacl_MAE_profit(ts, ts_refer):
    '''
    Task: Calculating % of MAE improvment!

    Parameters
    ----------
    ts : Series
        Research parameter values
    ts_refer : Series
        Reference parameter values.

    Returns
    -------
    mae_imp : float
        % of MAE improvement.
    '''
    try:
        mae_imp = 100 - ((ts / ts_refer) * 100)
    except ZeroDivisionError:
        mae_imp = 0
    return mae_imp
# End of function!


# Function 4 --> cacl_RMSE_profit
def cacl_RMSE_profit(ts, ts_refer):
    '''
    Task: Calculating % of RMSE improvment!

    Parameters
    ----------
    ts : Series
        Research parameter values
    ts_refer : Series
        Reference parameter values.

    Returns
    -------
    rmse_imp : float
        % of RMSE improvement.
    '''
    try:
        rmse_imp = 100 - ((ts / ts_refer) * 100)
    except ZeroDivisionError:
        rmse_imp = 0
    return rmse_imp
# End of function!


# Function 5 --> cal_stat_values
def cal_stat_values(df, lst4delta, refer):
    '''
    Task: Create output dataframe with statistical information for North Dvina
          model experiments!

    Parameters
    ----------
    df : DataFrame
        Initial dataframe with data
    lst4delta : List, str
        Columns for analysis
    refer : str
        Reference dataset (column).

    Returns
    -------
    df_stat : DataFrame
        Statistical dataframe.
    '''
    # Local variables:
    temp_refer_column = 'ecomag_meteo'

    # Calculations of temporal reference values:
    refer_delta = df[temp_refer_column] - df[refer]
    refer_mae   = calc_MAE(refer_delta)
    refer_rmse  = calc_RMSE(refer_delta)

    #-- Main calculations (including reference --> should be equal to 1)
    lst4stat_values = []
    for var in lst4delta:
        # Get DELTA (MODEL - REFER)
        tmp_delta = df[var] - df[refer]

        # Calculation of MEAN:
        var_mean = tmp_delta.mean()

        # Calculation of STD:
        var_std  = tmp_delta.std()

        # Calculation of MAE и RMSE:
        var_mae  = calc_MAE(tmp_delta)
        var_rmse = calc_RMSE(tmp_delta)

        # Calculation of improvement % for MAE and RMSE (ECOMAG метео = REFERENCE):
        var_mae_profit  = cacl_MAE_profit( var_mae , refer_mae )
        var_rmse_profit = cacl_RMSE_profit(var_rmse, refer_rmse)

        # Create list of dataframes with statistical values for parameter:
        lst4stat_values.append(pd.DataFrame(
            {f'{var}':[
                var_mean, var_std, var_mae, var_rmse, var_mae_profit, var_rmse_profit]},
            index = [
                'MEAN'  , 'STD'  , 'MAE'  , 'RMSE'  , '% MAE'       , '% RMSE'       ],
            )
        )
        # Create output dataset with statistical values:
        df_stat = pd.concat(lst4stat_values, axis = 1)

    return df_stat
# End of function!
