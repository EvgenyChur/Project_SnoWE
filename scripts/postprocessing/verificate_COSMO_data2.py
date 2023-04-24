# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:42:41 2018

@author: Churiulin Evgenii
Скрипт предназначен для считывания и работы с результатом статистической обработки (верификации модели COSMO-Ru на основе скрипта Дениса)
"""

import pandas as pd


#Путь к рассчитанной статистике по температуре воздуха
fileName_t_1 = 'vf_se_cm07etr_oper_t2m_2017120100_2018022821.txt' # Данные за зиму
fileName_t_2 = 'vf_se_cm07etr_oper_t2m_2018030100_2018053121.txt' # Данные за весну
fileName_t_3 = 'vf_se_cm07etr_oper_t2m_2018060100_2018083121.txt' # Данные за лето

iPath_1 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_t_1)
iPath_2 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_t_2)
iPath_3 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_t_3)



#Путь к рассчитанной статистике по температуре точкы росы
fileName_td_1 = 'vf_se_cm07etr_oper_td2m_2017120100_2018022821.txt' # Данные за зиму
fileName_td_2 = 'vf_se_cm07etr_oper_td2m_2018030100_2018053121.txt' # Данные за весну
fileName_td_3 = 'vf_se_cm07etr_oper_td2m_2018060100_2018083121.txt' # Данные за лето

iPath_4 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_td_1)
iPath_5 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_td_2)
iPath_6 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_td_3)



#Путь к статистике рассчитанной по осадкам
# данные в точке
fileName_prec_1 = 'stat_error_cm07etr_oper_TOT_PREC_2017120100_2018022821_tc.txt' # Данные за зиму
fileName_prec_2 = 'stat_error_cm07etr_oper_TOT_PREC_2018030100_2018053121_tc.txt' # Данные за весну
fileName_prec_3 = 'stat_error_cm07etr_oper_TOT_PREC_2018060100_2018083121_tc.txt' # Данные за лето

# данные в радиусе 15 км
fileName_prec_4 = 'stat_error_cm07etr_oper_TOT_PREC_av15km_2017120100_2018022821_tc.txt' # Данные за зиму
fileName_prec_5 = 'stat_error_cm07etr_oper_TOT_PREC_av15km_2018030100_2018053121_tc.txt' # Данные за весну
fileName_prec_6 = 'stat_error_cm07etr_oper_TOT_PREC_av15km_2018060100_2018083121_tc.txt' # Данные за лето

# данные в радиусе 30 км
fileName_prec_7 = 'stat_error_cm07etr_oper_TOT_PREC_mx30km_2017120100_2018022821_tc.txt' # Данные за зиму
fileName_prec_8 = 'stat_error_cm07etr_oper_TOT_PREC_mx30km_2018030100_2018053121_tc.txt' # Данные за весну
fileName_prec_9 = 'stat_error_cm07etr_oper_TOT_PREC_mx30km_2018060100_2018083121_tc.txt' # Данные за лето


# атмосферные осадки в точке, в радиусе 15 км, в радиусе 30 км (верификационные критерии)
iPath_prec_1 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_1)
iPath_prec_2 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_2)
iPath_prec_3 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_3)
iPath_prec_4 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_4)
iPath_prec_5 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_5)
iPath_prec_6 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_6)
iPath_prec_7 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_7)
iPath_prec_8 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_8)
iPath_prec_9 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_9)   



# атмосферные осадки в точке, в радиусе 15 км, в радиусе 30 км (статистические критерии)
# данные в точке
fileName_prec_lin_1 = 'vf_se_cm07etr_oper_TOT_PREC_2017120100_2018022821.txt'
fileName_prec_lin_2 = 'vf_se_cm07etr_oper_TOT_PREC_2018030100_2018053121.txt'
fileName_prec_lin_3 = 'vf_se_cm07etr_oper_TOT_PREC_2018060100_2018083121.txt'

# данные в радиусе 15 км
fileName_prec_lin_4 = 'vf_se_cm07etr_oper_TOT_PREC_av15km_2017120100_2018022821.txt'
fileName_prec_lin_5 = 'vf_se_cm07etr_oper_TOT_PREC_av15km_2018030100_2018053121.txt'
fileName_prec_lin_6 = 'vf_se_cm07etr_oper_TOT_PREC_av15km_2018060100_2018083121.txt'

# данные в радиусе 30 км
fileName_prec_lin_7 = 'vf_se_cm07etr_oper_TOT_PREC_mx30km_2017120100_2018022821.txt'
fileName_prec_lin_8 = 'vf_se_cm07etr_oper_TOT_PREC_mx30km_2018030100_2018053121.txt'
fileName_prec_lin_9 = 'vf_se_cm07etr_oper_TOT_PREC_mx30km_2018060100_2018083121.txt'


# атмосферные осадки в точке, в радиусе 15 км, в радиусе 30 км (верификационные критерии)
iPath_prec_lin_1 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_1)
iPath_prec_lin_2 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_2)
iPath_prec_lin_3 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_3)
iPath_prec_lin_4 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_4)
iPath_prec_lin_5 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_5)
iPath_prec_lin_6 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_6)
iPath_prec_lin_7 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_7)
iPath_prec_lin_8 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_8)
iPath_prec_lin_9 = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt/{}'.format(fileName_prec_lin_9)   




#Считывание данных по температуре
df_t_1 = pd.read_csv(iPath_1, comment ='#', sep = '\t')
df_t_2 = pd.read_csv(iPath_2, comment ='#', sep = '\t')
df_t_3 = pd.read_csv(iPath_3, comment ='#', sep = '\t')
                     
#Считывание данных по температуре точки росы
df_td_1 = pd.read_csv(iPath_4, comment ='#', sep = '\t')
df_td_2 = pd.read_csv(iPath_5, comment ='#', sep = '\t')
df_td_3 = pd.read_csv(iPath_6, comment ='#', sep = '\t')
                      
#Считывание данных по осадкам
df_prec_1 = pd.read_csv(iPath_prec_1, comment ='#', sep = '\t')
df_prec_2 = pd.read_csv(iPath_prec_2, comment ='#', sep = '\t')
df_prec_3 = pd.read_csv(iPath_prec_3, comment ='#', sep = '\t')
df_prec_4 = pd.read_csv(iPath_prec_4, comment ='#', sep = '\t')
df_prec_5 = pd.read_csv(iPath_prec_5, comment ='#', sep = '\t')
df_prec_6 = pd.read_csv(iPath_prec_6, comment ='#', sep = '\t')
df_prec_7 = pd.read_csv(iPath_prec_7, comment ='#', sep = '\t')
df_prec_8 = pd.read_csv(iPath_prec_8, comment ='#', sep = '\t')
df_prec_9 = pd.read_csv(iPath_prec_9, comment ='#', sep = '\t')
                      
                      
#Считывание данных по осадкам                 
df_prec_lin_1 = pd.read_csv(iPath_prec_lin_1, comment ='#', sep = '\t')
df_prec_lin_2 = pd.read_csv(iPath_prec_lin_2, comment ='#', sep = '\t')
df_prec_lin_3 = pd.read_csv(iPath_prec_lin_3, comment ='#', sep = '\t')
df_prec_lin_4 = pd.read_csv(iPath_prec_lin_4, comment ='#', sep = '\t')
df_prec_lin_5 = pd.read_csv(iPath_prec_lin_5, comment ='#', sep = '\t')
df_prec_lin_6 = pd.read_csv(iPath_prec_lin_6, comment ='#', sep = '\t')
df_prec_lin_7 = pd.read_csv(iPath_prec_lin_7, comment ='#', sep = '\t')
df_prec_lin_8 = pd.read_csv(iPath_prec_lin_8, comment ='#', sep = '\t')
df_prec_lin_9 = pd.read_csv(iPath_prec_lin_9, comment ='#', sep = '\t')                      
                      
    
