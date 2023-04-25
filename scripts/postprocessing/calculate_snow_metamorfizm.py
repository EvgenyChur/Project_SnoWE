# -*- coding: utf-8 -*-
"""
Description: Скрипт позволяющий разработанный с целью расчета скорости 
             деструктивного метаморфизма снежного покрова в условиях постоянно 
             изменяющегося шага по времени.

Authors: Evgenii Churiulin, Denis Blinov
                                                   
Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    06.06.2019 Evgenii Churiulin, RHMS
           Initial release
    1.2    25.04.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring 
"""
# =============================     Import modules     =====================
import pandas as pd
import numpy as np

import lib4system_suport as l4s
import lib4processing as l4p
# =============================   Personal functions   ====================
def create():
    '''
    Task: Create initial lists

    Returns
    -------
    var : float --> Temporal variable for research parameter 
    lst1 : list --> List for writing research parameter, except the fist moment of time
    lst2 : list --> List for writing research parameter, only for the fist moment of time
    lst3 : list --> List for lst1 + lst2
    ''' 
    var = 0.0
    lst1 = []
    lst2 = []
    lst3 = []
    return var, lst1, lst2, lst3

def clean(var:int, lst1:list, lst2:list, lst3:list):
    '''
    Task: Clean previous calculations

    Parameters
    ----------
    var  : temporal parameter
    lst1 : temporal list 1
    lst2 : temporal list 2
    lst3 : temporal list 3

    Returns
    -------
    var : temporal parameter
    '''
    var = 0.0
    lst1.clear()
    lst2.clear()
    lst3.clear()
    return var

# ================   User settings (have to be adapted)  ==================

# Input and output paths:
main = 'D:/Churyulin/germania'

pin  = main + '/Snow_1.xlsx'
pout = main + 'RESULTS'
      
# Local variables:
zero = 0.0

isum = -1
time = zero              # продолжительности случая, в часах
summa_delta_snow = zero  # суммарное изменения высоты снега
delta_snow = zero        # суммарное изменения высоты снега, по модулю
speed = zero             # скорость деформации на 1 шаге
speed_avg = zero         # средная скорость деформации за весь случай
deformation = zero       # скорость деформации
h_snow = zero            # исходная высота снега
sd = []                 # высота снега за период случая

# -- Create temporal variables for:
# a. T2m calculations:
temp_avg, temp_avg_list, temperatura_list_1step, result_temperatura = create()
# b. T2m_max calculations:
temp_max, temp_max_list, temperatura_max_list_1step, result_temperatura_max = create() 
# c. T2m_min calculations:
temp_min, temp_min_list, temperatura_min_list_1step, result_temperatura_min = create() 
# d. Wind speed
veter, veter_list, veter_list_1step, result_veter = create()

#=============================    Main program   ============================== 
if __name__ == '__main__':
    
    # Create output folder
    pout = l4s.makefolder(pout)
    
    # Cleaning previous results
    l4s.clean_history(pout)
    
    # Get data
    df = l4p.get_csv_data(pin)
    
    # Print columns:  
    print ('Columns:', df.columns)
    
    # Delete columns with unuseful data: 
    df = df.drop(
        ['ttt', 'info', 'hy'  , 'hj'   , 't_start', 't_stop', 'U1' , 'U2', 
         'U3' , 'U4'  , 'Ud'  , 'Udd'  , 'time'   , 'time.1', 'Tch', 'T' ,
         't'  , 'Vcr' , 'Vmax', 'delta'], axis = 1)
    
    
    df_2 = df[np.isfinite(df['hSnow       '])]
    
    df_3 = df
    df_3['delta_Snow'] = df_2['hSnow       '].diff().fillna(0).astype(int)
    
   
    df_3 = df.assign(delta_Time=df_2.index.to_series().diff().fillna(0).astype('timedelta64[h]'))
    df_3['speed'] = (df_3['delta_Snow']/df_3['delta_Time'])
    
    
    df_zero = np.full((len(df_3),8),np.nan)
    df_snow = pd.DataFrame(data=df_zero)
    # Rename columns:
    df_snow.columns = [
        'Time, hour'   , 'delta_sd, sm', 'U_def_avg, sm/hour', 'U_def, %/hour',
         'T2m avg'     , 'T2m max'     , 'T2m min'           , 'veter'        ]
    
    
    # -- Start main computations: 
    for i in range(len(df_3['delta_Snow'])):
        if  np.isnan(df_3['delta_Snow'][i]):
            #print(i)
            continue
        elif df_3['delta_Snow'][i] < 0 :
            #Расчет продолжительности всего случая
            time = time + df_3['delta_Time'][i]
            
            #Расчет суммарного изменения высоты снежного покрова в результате метаморфизма
            summa_delta_snow = (summa_delta_snow + df_3['delta_Snow'][i])
            delta_snow = summa_delta_snow * -1 #Перевод из отрицательной дельты в положительную
            
            #Расчет средней скорости деформации
            speed = (speed + ((-1 * df_3['speed'][i])*(df_3['delta_Time'][i])))    
            
            #Выборка h_snow_start
            h_snow = df_3['hSnow       '][i] #определение высоты свежевыпавшего снега
            #sd.append(h_snow) #список, с информацией о высоте снега
            #sd_start = sd[0] # первичная высота снега
            
            #Заполенения списка с температурами среднесуточными
            temp_avg = df_3['t2m         '][i]
            temp_avg_list.append(temp_avg)
            
            #Заполенения списка с температурами максимальными
            temp_max = df_3['tMax2m      '][i]
            temp_max_list.append(temp_max)
            
            #Заполенения списка с температурами минимальными
            temp_min = df_3['tMin2m      '][i]
            temp_min_list.append(temp_min)
            
            veter =  df_3['ff10m       '][i]
            veter_list.append(veter)
     
        elif df_3['delta_Snow'][i] >= 0 and summa_delta_snow < 0:
            isum = isum +1
          
            #Запись в массив. Переменная продолжительность случая
            df_snow['Time, hour'][isum] = time
           
            #Запись в массив. Переменная дельта снега - для случая
            df_snow['delta_sd, sm'][isum] = delta_snow
            
            #Запись в массив. Скорость деформации снега
            #Расчет скорости деформации
            speed_avg = speed / time
            df_snow['U_def_avg, sm/hour'][isum] = speed_avg
            
            #Запись в массив. Деформация снега
            
            # Расчет деформации
            deformation = ((delta_snow/sd_start)/time) * 100
            df_snow['U_def, %/hour'][isum] = deformation
    
            #Расчет среднесуточной температуры воздуха с учетом 1-го шага
            temperatura_list_1step.append(temperatura_avg)
            result_temperatura = temperatura_list_1step + temp_avg_list
            temp_avg_1 = np.nanmean(result_temperatura)
            df_snow['T2m avg'][isum] = temp_avg_1
            
            #Расчет максимальной температуры воздуха с учетом 1-го шага
            temperatura_max_list_1step.append(temperatura_max)
            result_temperatura_max = temperatura_max_list_1step + temp_max_list
            temp_max_1 = np.nanmax(result_temperatura_max)
            df_snow['T2m max'][isum] = temp_max_1
            
            #Расчет минимальной температуры воздуха с учетом 1-го шага
            temperatura_min_list_1step.append(temperatura_min)
            result_temperatura_min = temperatura_min_list_1step + temp_min_list
            temp_min_1 = np.nanmin(result_temperatura_min)
            df_snow['T2m min'][isum] = temp_min_1
    
            #Расчет скорости ветра с учетом 1-го шага
            veter_avg = np.mean(veter_list)
            
            veter_list_1step.append(veter_1_day)
            result_veter = veter_list_1step + veter_list
            veter_avg = np.nanmean(result_veter)
            df_snow['veter'][isum] = veter_avg         
            
            # -- Reset previous computations:
            time = zero
            summa_delta_snow = zero 
            delta_snow = zero
            speed = zero
            speed_avg = zero
            h_snow = zero
            deformation = zero         
              
            # -- Reset previous computations:   
            # T2m
            temp_avg = clean(temp_avg, temp_avg_list, temperatura_list_1step, result_temperatura)
            # T2m_max
            temp_max = clean(temp_max, temp_max_list, temperatura_max_list_1step, result_temperatura_max)
            # T2m_min
            temp_min = clean(temp_min, temp_min_list, temperatura_min_list_1step, result_temperatura_min)
            # Wind speed
            veter    = clean(veter, veter_list, veter_list_1step, result_veter)
    
            
            sd_start = df_3['hSnow       '][i] 
            temperatura_avg = df_3 ['t2m         '][i]
            temperatura_max = df_3['tMax2m      '][i]
            temperatura_min = df_3['tMin2m      '][i]
            veter_1_day = df_3['ff10m       '][i]
        
        elif df_3['delta_Snow'][i] >= 0 and summa_delta_snow == 0:
           sd_start = df_3['hSnow       '][i]
           temperatura_avg = df_3 ['t2m         '][i]
           temperatura_max = df_3['tMax2m      '][i]
           temperatura_min = df_3['tMin2m      '][i]
           veter_1_day = df_3['ff10m       '][i]
           
    #Удаление лишних строк       
    df_result = df_snow[np.isfinite(df_snow['delta_sd, sm'])]
    
    # Save output result in .csv file
    df_result.to_csv(
        f'{pout}/final.csv', sep = ';', float_format = '%.3f')

#=============================    End of program   ============================ 