# -*- coding: utf-8 -*-
"""
Created on Tue Dec 05 15:43:59 2017

@author: Evgeny Churiulin
Скрипт предназначенный для работы с данными маршрутных снегомерных наблюдений размещенных на сайте ВНИИГМИ МЦД meteo.ru
"""

import pandas as pd
import numpy as np
import os

#fileName_1 = '23445.txt'
#iPath_1 = 'C:/Python_script/Data_2017/Marshrut/Nadim/{}'.format(fileName_1)

def meteo_ru_swe(Path):
    
    #Работа с текстовым файлом
    widths = [5, 5, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 4, 4, 4, 5, 5, 3, 3] 
    df = pd.read_fwf(Path, widths=widths, header=None)
    #df = pd.read_table(iPath_1, header=None)
    # Id - индекс ВМО
    # Y - год
    # M - месяц
    # TM - тип маршрута
    # D - день
    # SPOSS - степеь покрытия окрерстности снеции снегом
    # SPMS - степень покрытия маршрута снегом
    # SPMLK - степень покрытия маршрута ледяной коркой
    # SVSPNM - средняя высота снежного покрова на маршруте (см)
    # NVSPNM - наибольшая высота снежного покрова на маршруте (см)
    # NminVSPNM - нименьшая высота снежного покрова на маршруте (см)
    # RHO - средняя плотность снега
    # STLK - средняя толщина ледяной корки
    # TSSNW - толщина слоя снега, насыщенного водой (мм)
    # TSCHW - толщина слоя чистой воды (мм)
    # SWE - запас воды в снеге (мм)
    # SWE_sum - общий запас воды в снеге (мм)
    # XZSP - характер залегания снежного покрова
    # XSP - хараетер снежного покрова
    df.columns = ['Id', 'Y', 'M', 'TM','D','SPOSS','SPMS','SPMLK','SVSPNM','NVSPNM','NminVSPNM','RHO','STLK','TSSNW','TSCHW','SWE','SWE_sum','XZSP','XSP']
    #print 'Columns:', df.columns
    #df=df.drop(['Id','A','AP','P','at'], axis=1)
    year = df.iloc[:,1]
    mon = df.iloc[:,2]
    day = df.iloc[:,4]
    meteo_dates = [pd.to_datetime('{}-{}-{}'.format(i, j, z), format='%Y-%m-%d') for i,j,z in zip(year, mon, day)]
    SWE = pd.Series(df['SWE'].values, index=meteo_dates)
    
    SWE = SWE.replace(9999, np.nan)
    SWE = SWE.groupby(level=0)
    SWE = SWE.mean()
    #return meteo_dates
    #return Id
    return SWE

# Данные для реки Надым

iPath_1 = 'C:/Python_script/Data_2017/Marshrut/Nadim/'
dirs_meteo = os.listdir(iPath_1)
for i in dirs_meteo:
    print (i)
    
fileName_1 = '23445.txt' 
data1 = meteo_ru_swe(iPath_1+fileName_1)

#Cоединяем данные в один датафрейм - Надым
data1.index
df_data = pd.concat([data1], axis = 1)
df_data.columns = ['23445']

df_data['mean'] = df_data.mean(axis = 1)

#Работа с excel
#сохранение в MS Excel и текстовый файл
df_data.to_excel('C:/Python_script/Data_2017/Marshrut/Nadim/result_Nadim.xlsx', float_format = '%.1f', header = ['23445','mean'], index_label = 'Time')


#Данные для реки Онега
iPath_2 = 'C:/Python_script/Data_2017/Marshrut/Onega/'
dirs_meteo = os.listdir(iPath_2)
for i in dirs_meteo:
    print (i)
    
fileName_2 = '22641.txt' 
fileName_3 = '22648.txt' 
fileName_4 = '22845.txt' 
fileName_5 = '22854.txt' 
fileName_6 = '22954.txt' 
data2 = meteo_ru_swe(iPath_2+fileName_2)
data3 = meteo_ru_swe(iPath_2+fileName_3)
data4 = meteo_ru_swe(iPath_2+fileName_4)
data5 = meteo_ru_swe(iPath_2+fileName_5)
data6 = meteo_ru_swe(iPath_2+fileName_6)

df_data_onega = data6.to_frame('22954')
df_data_onega = df_data_onega.assign(S_22641 = data2, S_22648 = data3, S_22854 = data5, S_22845 = data4)
df_data_onega['mean'] = df_data_onega.mean(axis = 1)
#Работа с excel
#сохранение в MS Excel и текстовый файл
df_data_onega.to_excel('C:/Python_script/Data_2017/Marshrut/Onega/result_Onega.xlsx', float_format = '%.1f', header = ['22954','22641','22648','22854','22845','mean'], index_label = 'Time')

#Данные для реки Дон
iPath_3 = 'C:/Python_script/Data_2017/Marshrut/Don/'
dirs_meteo = os.listdir(iPath_3)
for i in dirs_meteo:
    print (i)

fileName_7 = '27858.txt' 
fileName_8 = '27921.txt' 
fileName_9 = '27928.txt' 
fileName_10 = '27930.txt' 
fileName_11 = '27935.txt'
fileName_12 = '27957.txt' 
fileName_13 = '34013.txt' 
fileName_14 = '34056.txt' 
fileName_15 = '34063.txt' 
fileName_16 = '34069.txt'
fileName_17 = '34116.txt' 
fileName_18 = '34146.txt' 
fileName_19 = '34152.txt' 
fileName_20 = '34163.txt' 
fileName_21 = '34238.txt'
fileName_22 = '34247.txt' 
fileName_23 = '34321.txt' 
fileName_24 = '34336.txt' 
fileName_25 = '34432.txt' 
fileName_26 = '34740.txt' 
data7 = meteo_ru_swe(iPath_3+fileName_7)
data8 = meteo_ru_swe(iPath_3+fileName_8)
data9 = meteo_ru_swe(iPath_3+fileName_9)
data10 = meteo_ru_swe(iPath_3+fileName_10)
data11 = meteo_ru_swe(iPath_3+fileName_11)
data12 = meteo_ru_swe(iPath_3+fileName_12)
data13 = meteo_ru_swe(iPath_3+fileName_13)
data14 = meteo_ru_swe(iPath_3+fileName_14)
data15 = meteo_ru_swe(iPath_3+fileName_15)
data16 = meteo_ru_swe(iPath_3+fileName_16)
data17 = meteo_ru_swe(iPath_3+fileName_17)
data18 = meteo_ru_swe(iPath_3+fileName_18)
data19 = meteo_ru_swe(iPath_3+fileName_19)
data20 = meteo_ru_swe(iPath_3+fileName_20)
data21 = meteo_ru_swe(iPath_3+fileName_21)
data22 = meteo_ru_swe(iPath_3+fileName_22)
data23 = meteo_ru_swe(iPath_3+fileName_23)
data24 = meteo_ru_swe(iPath_3+fileName_24)
data25 = meteo_ru_swe(iPath_3+fileName_25)
data26 = meteo_ru_swe(iPath_3+fileName_26)

df_data_don = data11.to_frame('27935')
df_data_don = df_data_don.assign(S_27858 = data7, S_27921 = data8, S_27928 = data9, S_27930 = data10,
                                 S_27957 = data12, S_34013 = data13, S_34056 = data14, S_34063 = data15,
                                 S_34069 = data16, S_34116 = data17, S_34146 = data18, S_34321 = data23,
                                 S_34336 = data24, S_34432 = data25, S_34740 = data26, S_34163 = data20,
                                 S_34247 = data22, S_34152 = data19 )

df_data_don['mean'] = df_data_don.mean(axis = 1)
#Работа с excel
#сохранение в MS Excel и текстовый файл
df_data_don.to_excel('C:/Python_script/Data_2017/Marshrut/Don/result_Don.xlsx',
                     float_format = '%.1f', header = ['27935','S_27858','S_27921','S_27928','S_27930',
                                                      'S_27957','S_34013','S_34056','S_34063','S_34069',
                                                      'S_34116','S_34146','S_34321','S_34336','S_34432',
                                                      'S_34740','S_34163','S_34247','S_34152','mean'], index_label = 'Time')


#Данные для реки Северная Двина
iPath_4 = 'C:/Python_script/Data_2017/Marshrut/Dvina/'
dirs_meteo = os.listdir(iPath_4)
#for i in dirs_meteo:
#    print i

#fileName = dirs_meteo[0:len(dirs_meteo)-1]

fileName_27 = '22271.txt' 
fileName_28 = '22292.txt' 
fileName_29 = '22365.txt' 
fileName_30 = '22383.txt' 
fileName_31 = '22438.txt'
fileName_32 = '22471.txt' 
fileName_33 = '22541.txt' 
fileName_34 = '22559.txt' 
fileName_35 = '22563.txt' 
fileName_36 = '22573.txt'
fileName_37 = '22648.txt' 
fileName_38 = '22656.txt' 
fileName_39 = '22676.txt' 
fileName_40 = '22686.txt' 
fileName_41 = '22695.txt'
fileName_42 = '22762.txt' 
fileName_43 = '22778.txt' 
fileName_44 = '22798.txt' 
fileName_45 = '22831.txt' 
fileName_46 = '22845.txt' 
fileName_47 = '22854.txt'
fileName_48 = '22867.txt' 
fileName_49 = '22981.txt' 
fileName_50 = '22996.txt' 
fileName_51 = '23207.txt' 
fileName_52 = '23226.txt'
fileName_53 = '23305.txt' 
fileName_54 = '23330.txt' 
fileName_55 = '23412.txt' 
fileName_56 = '23518.txt'
fileName_57 = '23606.txt' 
fileName_58 = '23701.txt' 
fileName_59 = '23803.txt' 
fileName_60 = '27026.txt' 
fileName_61 = '27051.txt'
fileName_62 = '27066.txt' 
fileName_63 = '27083.txt' 
fileName_64 = '27097.txt' 
fileName_65 = '27242.txt'
fileName_66 = '27243.txt' 
fileName_67 = '27252.txt' 
fileName_68 = '27271.txt' 
"""
data = ['']*len(fileName)
for i in xrange(len(fileName)):
    data[i] = meteo_ru_swe(iPath_4+fileName[i])
"""
data27 = meteo_ru_swe(iPath_4+fileName_27)
data28 = meteo_ru_swe(iPath_4+fileName_28)
data29 = meteo_ru_swe(iPath_4+fileName_29)
data30 = meteo_ru_swe(iPath_4+fileName_30)
data31 = meteo_ru_swe(iPath_4+fileName_31)
data32 = meteo_ru_swe(iPath_4+fileName_32)
data33 = meteo_ru_swe(iPath_4+fileName_33)
data34 = meteo_ru_swe(iPath_4+fileName_34)
data35 = meteo_ru_swe(iPath_4+fileName_35)
data36 = meteo_ru_swe(iPath_4+fileName_36)
data37 = meteo_ru_swe(iPath_4+fileName_37)
data38 = meteo_ru_swe(iPath_4+fileName_38)
data39 = meteo_ru_swe(iPath_4+fileName_39)
data40 = meteo_ru_swe(iPath_4+fileName_40)
data41 = meteo_ru_swe(iPath_4+fileName_41)
data42 = meteo_ru_swe(iPath_4+fileName_42)
data43 = meteo_ru_swe(iPath_4+fileName_43)
data44 = meteo_ru_swe(iPath_4+fileName_44)
data45 = meteo_ru_swe(iPath_4+fileName_45)
data46 = meteo_ru_swe(iPath_4+fileName_46)
data47 = meteo_ru_swe(iPath_4+fileName_47)
data48 = meteo_ru_swe(iPath_4+fileName_48)
data49 = meteo_ru_swe(iPath_4+fileName_49)
data50 = meteo_ru_swe(iPath_4+fileName_50)
data51 = meteo_ru_swe(iPath_4+fileName_51)
data52 = meteo_ru_swe(iPath_4+fileName_52)
data53 = meteo_ru_swe(iPath_4+fileName_53)
data54 = meteo_ru_swe(iPath_4+fileName_54)
data55 = meteo_ru_swe(iPath_4+fileName_55)
data56 = meteo_ru_swe(iPath_4+fileName_56)
data57 = meteo_ru_swe(iPath_4+fileName_57)
data58 = meteo_ru_swe(iPath_4+fileName_58)
data59 = meteo_ru_swe(iPath_4+fileName_59)
data60 = meteo_ru_swe(iPath_4+fileName_60)
data61 = meteo_ru_swe(iPath_4+fileName_61)
data62 = meteo_ru_swe(iPath_4+fileName_62)
data63 = meteo_ru_swe(iPath_4+fileName_63)
data64 = meteo_ru_swe(iPath_4+fileName_64)
data65 = meteo_ru_swe(iPath_4+fileName_65)
data66 = meteo_ru_swe(iPath_4+fileName_66)
data67 = meteo_ru_swe(iPath_4+fileName_67)
data68 = meteo_ru_swe(iPath_4+fileName_68)

df_data_dvina = data64.to_frame('27097')

df_data_dvina = df_data_dvina.assign(S_22271 = data27, S_22292 = data28, S_22365 = data29, S_22383 = data30, S_22438 = data31,
                                     S_22471 = data32, S_22541 = data33, S_22559 = data34, S_22573 = data36, S_22648 = data37,
                                     S_22656 = data38, S_22676 = data39, S_22695 = data41, S_22981 = data49, S_23606 = data57,
                                     S_27026 = data60, S_27243 = data66, S_27271 = data68, S_22854 = data47, S_23207 = data51,
                                     S_23226 = data52, S_23305 = data53, S_23330 = data54, S_23412 = data55, S_23518 = data56,
                                     S_22563 = data35, S_22686 = data40, S_22762 = data42, S_22845 = data46, S_22778 = data43,
                                     S_22798 = data44, S_22831 = data45, S_22867 = data48, S_22996 = data50, S_27242 = data65,
                                     S_23701 = data58, S_23803 = data59, S_27051 = data61, S_27066 = data62, S_27083 = data63,
                                     S_27252 = data67)



df_data_dvina['mean'] = df_data_dvina.mean(axis = 1)
#Работа с excel
#сохранение в MS Excel и текстовый файл
df_data_dvina.to_excel('C:/Python_script/Data_2017/Marshrut/Dvina/result_Dvina.xlsx', float_format = '%.1f', header = ['S_27097','S_22271', 'S_22292', 'S_22365', 'S_22383', 'S_22438',
                                                                                                                       'S_22471','S_22541', 'S_22559', 'S_22573', 'S_22648', 'S_22656',
                                                                                                                       'S_22676','S_22695', 'S_22981', 'S_23606', 'S_27026', 'S_27243',
                                                                                                                       'S_27271','S_22854', 'S_23207', 'S_23226', 'S_23305', 'S_23330',
                                                                                                                       'S_23412','S_23518', 'S_22563', 'S_22686', 'S_22762', 'S_22845', 
                                                                                                                       'S_22778','S_22798', 'S_22831', 'S_22867', 'S_22996', 'S_27242',
                                                                                                                       'S_23701','S_23803', 'S_27051', 'S_27066', 'S_27083', 'S_27252','mean'], index_label = 'Time')

                                                                                                                    
#Блок кода для реки Северная Двина
iPath_5 = 'C:/Python_script/Data_2017/Marshrut/Oka/'
dirs_meteo = os.listdir(iPath_5)
for i in dirs_meteo:
    print (i)

fileName_69 = '26499.txt' 
fileName_70 = '26695.txt' 
fileName_71 = '26795.txt' 
fileName_72 = '26882.txt' 
fileName_73 = '26894.txt'
fileName_74 = '26896.txt' 
fileName_75 = '26898.txt' 
fileName_76 = '27321.txt' 
fileName_77 = '27329.txt' 
fileName_78 = '27333.txt'
fileName_79 = '27346.txt' 
fileName_80 = '27355.txt' 
fileName_81 = '27402.txt' 
fileName_82 = '27417.txt' 
fileName_83 = '27428.txt'
fileName_84 = '27441.txt' 
fileName_85 = '27462.txt' 
fileName_86 = '27502.txt' 
fileName_87 = '27509.txt' 
fileName_88 = '27511.txt' 
fileName_89 = '27523.txt'
fileName_90 = '27606.txt' 
fileName_91 = '27611.txt' 
fileName_92 = '27618.txt' 
fileName_93 = '27625.txt' 
fileName_94 = '27643.txt'
fileName_95 = '27648.txt' 
fileName_96 = '27653.txt' 
fileName_97 = '27665.txt' 
fileName_98 = '27703.txt'
fileName_99 = '27707.txt' 
fileName_100 = '27719.txt' 
fileName_101 = '27729.txt' 
fileName_102 = '27736.txt' 
fileName_103 = '27745.txt'
fileName_104 = '27752.txt' 
fileName_105 = '27758.txt' 
fileName_106 = '27760.txt' 
fileName_107 = '27821.txt'
fileName_108 = '27823.txt' 
fileName_109 = '27835.txt' 
fileName_110 = '27848.txt' 
fileName_111 = '27858.txt' 
fileName_112 = '27921.txt' 
fileName_113 = '27930.txt' 
fileName_114 = '27935.txt'
fileName_115 = '27957.txt' 
fileName_116 = '27962.txt' 
fileName_117 = '34003.txt' 
fileName_118 = '34238.txt' 

data69 = meteo_ru_swe(iPath_5+fileName_69)
data70 = meteo_ru_swe(iPath_5+fileName_70)
data71 = meteo_ru_swe(iPath_5+fileName_71)
data72 = meteo_ru_swe(iPath_5+fileName_72)
data73 = meteo_ru_swe(iPath_5+fileName_73)
data74 = meteo_ru_swe(iPath_5+fileName_74)
data75 = meteo_ru_swe(iPath_5+fileName_75)
data76 = meteo_ru_swe(iPath_5+fileName_76)
data77 = meteo_ru_swe(iPath_5+fileName_77)
data78 = meteo_ru_swe(iPath_5+fileName_78)
data79 = meteo_ru_swe(iPath_5+fileName_79)
data80 = meteo_ru_swe(iPath_5+fileName_80)
data81 = meteo_ru_swe(iPath_5+fileName_81)
data82 = meteo_ru_swe(iPath_5+fileName_82)
data83 = meteo_ru_swe(iPath_5+fileName_83)
data84 = meteo_ru_swe(iPath_5+fileName_84)
data85 = meteo_ru_swe(iPath_5+fileName_85)
data86 = meteo_ru_swe(iPath_5+fileName_86)
data87 = meteo_ru_swe(iPath_5+fileName_87)
data88 = meteo_ru_swe(iPath_5+fileName_88)
data89 = meteo_ru_swe(iPath_5+fileName_89)
data90 = meteo_ru_swe(iPath_5+fileName_90)
data91 = meteo_ru_swe(iPath_5+fileName_91)
data92 = meteo_ru_swe(iPath_5+fileName_92)
data93 = meteo_ru_swe(iPath_5+fileName_93)
data94 = meteo_ru_swe(iPath_5+fileName_94)
data95 = meteo_ru_swe(iPath_5+fileName_95)
data96 = meteo_ru_swe(iPath_5+fileName_96)
data97 = meteo_ru_swe(iPath_5+fileName_97)
data98 = meteo_ru_swe(iPath_5+fileName_98)
data99 = meteo_ru_swe(iPath_5+fileName_99)
data100 = meteo_ru_swe(iPath_5+fileName_100)
data101 = meteo_ru_swe(iPath_5+fileName_101)
data102 = meteo_ru_swe(iPath_5+fileName_102)
data103 = meteo_ru_swe(iPath_5+fileName_103)
data104 = meteo_ru_swe(iPath_5+fileName_104)
data105 = meteo_ru_swe(iPath_5+fileName_105)
data106 = meteo_ru_swe(iPath_5+fileName_106)
data107 = meteo_ru_swe(iPath_5+fileName_107)
data108 = meteo_ru_swe(iPath_5+fileName_108)
data109 = meteo_ru_swe(iPath_5+fileName_109)
data110 = meteo_ru_swe(iPath_5+fileName_110)
data111 = meteo_ru_swe(iPath_5+fileName_111)
data112 = meteo_ru_swe(iPath_5+fileName_112)
data113 = meteo_ru_swe(iPath_5+fileName_113)
data114 = meteo_ru_swe(iPath_5+fileName_114)
data115 = meteo_ru_swe(iPath_5+fileName_115)
data116 = meteo_ru_swe(iPath_5+fileName_116)
data117 = meteo_ru_swe(iPath_5+fileName_117)
data118 = meteo_ru_swe(iPath_5+fileName_118)


df_data_oka = data116.to_frame('27962')

df_data_oka = df_data_oka.assign(S_26499 = data69, S_27333 = data78, S_27502 = data86, S_27643 = data94, S_27736 = data102,
                                 S_26695 = data70, S_27346 = data79, S_27509 = data87, S_27648 = data95, S_27745 = data103,
                                 S_26795 = data71, S_27355 = data80, S_27511 = data88, S_27653 = data96, S_27752 = data104,
                                 S_26882 = data72, S_27402 = data81, S_27523 = data89, S_27665 = data97, S_27758 = data105,
                                 S_26894 = data73, S_27417 = data82, S_27606 = data90, S_27703 = data98, S_27760 = data106,
                                 S_26896 = data74, S_27428 = data83, S_27611 = data91, S_27707 = data99, S_27821 = data107,
                                 S_26898 = data75, S_27441 = data84, S_27618 = data92, S_27719 = data100, S_27823 = data108,
                                 S_27321 = data76, S_27462 = data85, S_27625 = data93, S_27729 = data101, S_27835 = data109,
                                 S_27329 = data77, S_27848 = data110, S_27858 = data111, S_27921 = data112, S_27930 = data113,
                                 S_27935 = data114, S_27957 = data115, S_27962 = data116, S_34003 = data117, S_34238 = data118)


df_data_oka['mean'] = df_data_oka.mean(axis = 1)
#Работа с excel
#сохранение в MS Excel и текстовый файл
df_data_oka.to_excel('C:/Python_script/Data_2017/Marshrut/Oka/result_Oka.xlsx', float_format = '%.1f', header = ['S_26499', 'S_27333', 'S_27502', 'S_27643', 'S_27736',
                                                                                                                 'S_26695', 'S_27346', 'S_27509', 'S_27648', 'S_27745',
                                                                                                                'S_26795', 'S_27355', 'S_27511', 'S_27653', 'S_27752',
                                                                                                                 'S_26882', 'S_27402', 'S_27523', 'S_27665', 'S_27758',
                                                                                                                 'S_26894', 'S_27417', 'S_27606', 'S_27703', 'S_27760',
                                                                                                                 'S_26896', 'S_27428', 'S_27611', 'S_27707', 'S_27821',
                                                                                                                 'S_26898', 'S_27441', 'S_27618', 'S_27719', 'S_27823',
                                                                                                                 'S_27321', 'S_27462', 'S_27625', 'S_27729', 'S_27835',
                                                                                                                 'S_27329', 'S_27848', 'S_27858', 'S_27921', 'S_27930',
                                                                                                                 'S_27935','S_27957' , 'S_27962', 'S_34003', 'S_34238',
                                                                                                                 'S_27962','mean'], index_label = 'Time')                                                                                                                       
                                                                                                                       
                                                                                                                       
