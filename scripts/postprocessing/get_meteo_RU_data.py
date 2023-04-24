# -*- coding: utf-8 -*-
"""
Created on Sat Dec 02 21:48:55 2017

@author: Evgeny Churiulin
Инструмент позволяющий обрабатывать данные о высоте снежного покрова, полученных с сайта ВНИИГМИ МЦД meteo.ru
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
def replace(lst, number):
    for row in lst:
        for i, val in enumerate(row):
            if val == number:
                row[i] = '0'
    return lst

def meteo_ru(Path):
    #Работа с текстовым файлом
    widths = [5, 5, 3, 3, 5, 3, 2, 2, 2] 
    df = pd.read_fwf(Path, widths=widths, header=None)
    df.columns = ['Id', 'Y', 'M', 'D','SD','A','AP','P','at']
    #print 'Columns:', df.columns
    #df=df.drop(['Id','A','AP','P','at'], axis=1)
    year = df.iloc[:,1]
    mon = df.iloc[:,2]
    day = df.iloc[:,3]
    meteo_dates = [pd.to_datetime('{}-{}-{}'.format(i, j, z), format='%Y-%m-%d') for i,j,z in zip(year, mon,day)] 

    SD = pd.Series(df['SD'].values, index=meteo_dates)
    SD = SD.replace(9999, np.nan)
    ty = SD.resample('W').mean()
    #ty = y.to_frame()
    #ty['mean'] = ty.mean(axis = 1)
    return ty

#Данные по реке Северная Двина   
iPath_1 = 'C:/Python_script/Data_2017/Meteo_ru_field/Dvina/'
dirs_meteo = os.listdir(iPath_1)
for i in dirs_meteo:
    print (i)

# Список метеостанций   
fileName_1 = '22271.txt' 
fileName_2 = '22438.txt'
fileName_3 = '22471.txt'
fileName_4 = '22676.txt'
fileName_5 = '22768.txt'
fileName_6 = '22845.txt'
fileName_7 = '22854.txt'
fileName_8 = '22981.txt'
fileName_9 = '23330.txt'
fileName_10 = '23412.txt'
fileName_11 = '23914.txt'
fileName_12 = '27051.txt'
fileName_13 = '27066.txt'
fileName_14 = '27083.txt'
fileName_15 = '27164.txt'
fileName_16 = '27199.txt'
fileName_17 = '28009.txt'  

# Считываем данные метеостанций
data1 = meteo_ru(iPath_1 + fileName_1)
data2 = meteo_ru(iPath_1 + fileName_2)
data3 = meteo_ru(iPath_1 + fileName_3)
data4 = meteo_ru(iPath_1 + fileName_4)
data5 = meteo_ru(iPath_1 + fileName_5)
data6 = meteo_ru(iPath_1 + fileName_6)
data7 = meteo_ru(iPath_1 + fileName_7)
data8 = meteo_ru(iPath_1 + fileName_8)
data9 = meteo_ru(iPath_1 + fileName_9)
data10 = meteo_ru(iPath_1 + fileName_10)
data11 = meteo_ru(iPath_1 + fileName_11)
data12 = meteo_ru(iPath_1 + fileName_12)
data13 = meteo_ru(iPath_1 + fileName_13)
data14 = meteo_ru(iPath_1 + fileName_14)
data15 = meteo_ru(iPath_1 + fileName_15)
data16 = meteo_ru(iPath_1 + fileName_16)
data17 = meteo_ru(iPath_1 + fileName_17)

#Cоединяем данные в один датафрейм - Северная Двина
data1.index = data2.index = data3.index = data4.index = data5.index = data6.index = data7.index = data8.index = data9.index = data10.index = data11.index = data12.index = data13.index = data14.index = data15.index = data16.index = data17.index 
df_data_dvina = pd.concat([data1, data2, data3, data4, data5, data6, data7,
                           data8, data9, data10, data11, data12, data13, data14,
                           data15, data16, data17], axis = 1)
df_data_dvina.columns = ['22271','22438','22471','22676','22768','22845','22854',
                         '22981','23330','23412','23914','27051','27066','27083',
                         '27164','27199','28009']

df_data_dvina['mean'] = df_data_dvina.mean(axis = 1)

#Работа с excel Северная двина
df_data_dvina.to_excel('C:/Python_script/Data_2017/Meteo_ru_field/Dvina/result_Dvina.xlsx', float_format = '%.1f', 
                       header = ['22271','22438','22471','22676','22768','22845','22854','22981','23330','23412',
                                 '23914','27051','27066','27083','27164','27199','28009','mean'], index_label = 'Time')


#Данные по реке Ока  
iPath_2 = 'C:/Python_script/Data_2017/Meteo_ru_field/Oka/'
dirs_meteo2 = os.listdir(iPath_2)
for i in dirs_meteo2:
    print (i)
    
fileName_18 = '26499.txt' 
fileName_19 = '26898.txt'  
fileName_20 = '27333.txt'
fileName_21 = '27425.txt'
fileName_22 = '27459.txt'
fileName_23 = '27509.txt'
fileName_24 = '27612.txt'
fileName_25 = '27625.txt'
fileName_26 = '27648.txt'
fileName_27 = '27665.txt'
fileName_28 = '27707.txt'
fileName_29 = '27730.txt'
fileName_30 = '27756.txt'
fileName_31 = '27814.txt'
fileName_32 = '27823.txt'
fileName_33 = '27857.txt'
fileName_34 = '27935.txt'
fileName_35 = '27947.txt'
fileName_36 = '27962.txt'
fileName_37 = '34003.txt'
fileName_38 = '34009.txt'
fileName_39 = '34056.txt'

data18 = meteo_ru(iPath_2 + fileName_18)
data19 = meteo_ru(iPath_2 + fileName_19)
data20 = meteo_ru(iPath_2 + fileName_20)
data21 = meteo_ru(iPath_2 + fileName_21)
data22 = meteo_ru(iPath_2 + fileName_22)
data23 = meteo_ru(iPath_2 + fileName_23)
data24 = meteo_ru(iPath_2 + fileName_24)
data25 = meteo_ru(iPath_2 + fileName_25)
data26 = meteo_ru(iPath_2 + fileName_26)
data27 = meteo_ru(iPath_2 + fileName_27)
data28 = meteo_ru(iPath_2 + fileName_28)
data29 = meteo_ru(iPath_2 + fileName_29)
data30 = meteo_ru(iPath_2 + fileName_30)
data31 = meteo_ru(iPath_2 + fileName_31)
data32 = meteo_ru(iPath_2 + fileName_32)
data33 = meteo_ru(iPath_2 + fileName_33)
data34 = meteo_ru(iPath_2 + fileName_34)
data35 = meteo_ru(iPath_2 + fileName_35)
data36 = meteo_ru(iPath_2 + fileName_36)
data37 = meteo_ru(iPath_2 + fileName_37)
data38 = meteo_ru(iPath_2 + fileName_38)
data39 = meteo_ru(iPath_2 + fileName_39)


#соединяем данные в один датафрейм по Оке
data18.index = data19.index = data20.index = data21.index = data22.index = data23.index = data24.index = data25.index = data26.index = data27.index = data28.index = data29.index = data30.index = data31.index = data32.index = data33.index = data34.index = data35.index = data36.index = data37.index = data38.index = data39.index
df_data_oka = pd.concat([data18, data19, data20, data21, data22, data23, data24, data25, data26, data27,
                         data28, data29, data30, data31, data32, data33, data34, data35, data36, data37,
                         data38, data39], axis = 1)

df_data_oka.columns = ['26499','26898','27333','27425','27459','27509','27612','27625','27648','27665',
                       '27707','27730','27756','27814','27823','27857','27935','27947','27962','34003',
                       '34009','34056']

df_data_oka['mean'] = df_data_oka.mean(axis = 1)

#Работа с excel
df_data_oka.to_excel('C:/Python_script/Data_2017/Meteo_ru_field/Oka/result_Oka.xlsx', float_format = '%.1f', 
                     header = ['26499','26898','27333','27425','27459','27509','27612','27625','27648','27665',
                               '27707','27730','27756','27814','27823','27857','27935','27947','27962','34003',
                               '34009','34056','mean'], index_label = 'Time')

#Данные по реке Дон  
iPath_3 = 'C:/Python_script/Data_2017/Meteo_ru_field/Don/'
dirs_meteo3 = os.listdir(iPath_3)
for i in dirs_meteo3:
    print (i)
   
fileName_40 = '27935.txt' 
fileName_41 = '34056.txt'  
fileName_42 = '34059.txt'
fileName_43 = '34110.txt'
fileName_44 = '34123.txt'
fileName_45 = '34139.txt'
fileName_46 = '34152.txt'
fileName_47 = '34163.txt'
fileName_48 = '34240.txt'
fileName_49 = '34247.txt'
fileName_50 = '34321.txt'
fileName_51 = '34356.txt'
fileName_52 = '34432.txt'
fileName_53 = '34646.txt'
fileName_54 = '34720.txt'
fileName_55 = '34730.txt'
fileName_56 = '34740.txt'
fileName_57 = '34759.txt'
fileName_58 = '37031.txt'

data40 = meteo_ru(iPath_3 + fileName_40)
data41 = meteo_ru(iPath_3 + fileName_41)
data42 = meteo_ru(iPath_3 + fileName_42)
data43 = meteo_ru(iPath_3 + fileName_43)
data44 = meteo_ru(iPath_3 + fileName_44)
data45 = meteo_ru(iPath_3 + fileName_45)
data46 = meteo_ru(iPath_3 + fileName_46)
data47 = meteo_ru(iPath_3 + fileName_47)
data48 = meteo_ru(iPath_3 + fileName_48)
data49 = meteo_ru(iPath_3 + fileName_49)
data50 = meteo_ru(iPath_3 + fileName_50)
data51 = meteo_ru(iPath_3 + fileName_51)
data52 = meteo_ru(iPath_3 + fileName_52)
data53 = meteo_ru(iPath_3 + fileName_53)
data54 = meteo_ru(iPath_3 + fileName_54)
data55 = meteo_ru(iPath_3 + fileName_55)
data56 = meteo_ru(iPath_3 + fileName_56)
data57 = meteo_ru(iPath_3 + fileName_57)
data58 = meteo_ru(iPath_3 + fileName_58)

#Соединяем данные в один датафрейм - Дон
data40.index = data41.index = data42.index = data43.index = data44.index = data45.index = data46.index = data47.index = data48.index = data49.index = data50.index = data51.index = data52.index = data53.index = data54.index = data55.index = data56.index = data57.index = data58.index
df_data_don = pd.concat([data40, data41, data42, data43, data44, data45, data46, data47, data48, data49, 
                         data50, data51, data52, data53, data54, data55, data56, data57, data58], axis = 1)
df_data_don.columns = ['27935','34056','34059','34110','34123','34139','34152','34163','34240',
                       '34247','34321','34356','34432','34646','34720','34730','34740','34759','37031']
df_data_don['mean'] = df_data_don.mean(axis = 1)

#Работа с excel
df_data_don.to_excel('C:/Python_script/Data_2017/Meteo_ru_field/Don/result_Don.xlsx', float_format = '%.1f', 
                     header = ['27935','34056','34059','34110','34123','34139','34152','34163','34240',
                               '34247','34321','34356','34432','34646','34720','34730','34740','34759',
                               '37031','mean'], index_label = 'Time')

#Данные по реке Онеге  
iPath_4 = 'C:/Python_script/Data_2017/Meteo_ru_field/Onega/'
dirs_meteo4 = os.listdir(iPath_4)
for i in dirs_meteo4:
    print (i)

fileName_59 = '22641.txt' 
fileName_60 = '22854.txt'
data59 = meteo_ru(iPath_4 + fileName_59)
data60 = meteo_ru(iPath_4 + fileName_60)

#Cоединяем данные в один датафрейм - Онега
data59.index = data60.index
df_data_onega = pd.concat([data59, data60], axis = 1)
df_data_onega.columns = ['22641','22854']

df_data_onega['mean'] = df_data_onega.mean(axis = 1)
#Работа с excel for Onega catchment area
df_data_onega.to_excel('C:/Python_script/Data_2017/Meteo_ru_field/Onega/result_Onega.xlsx', float_format = '%.1f', 
                       header = ['22641','22854','mean'], index_label = 'Time')

#Данные по реке Надым
iPath_5 = 'C:/Python_script/Data_2017/Meteo_ru_field/Nadim/'
dirs_meteo5 = os.listdir(iPath_5)
for i in dirs_meteo5:
    print (i)
  
fileName_61 = '23445.txt' 
data61 = meteo_ru(iPath_5 + fileName_61)

#Cоединяем данные в один датафрейм - Надым
data61.index
df_data_nadim = pd.concat([data61], axis = 1)
df_data_nadim.columns = ['23445']

df_data_nadim['mean'] = df_data_nadim.mean(axis = 1)

#Работа с excel for catchment area Nadim
df_data_nadim.to_excel('C:/Python_script/Data_2017/Meteo_ru_field/Nadim/result_Nadim.xlsx', float_format = '%.1f',
                       header = ['23445','mean'], index_label = 'Time')


#Работа с графиком
plt.style.use('ggplot')
fig = plt.figure(figsize = (12,8))
ax1 = fig.add_subplot(111)
ax1 = plt.bar(df_data_don.index, df_data_don['mean'], color = 'k', align = 'center')

#a#x1 = plt.streamplot(df_data_nadim['mean'], df_data_nadim.index, 'b^')
#adf_data_nadim.plot(x='mean', y = df_data_nadim.index, kind = 'scatter')
plt.title(u'Изменение высоты снежного покрова в бассейне р. Дон ', fontsize=20, color = 'k')
plt.xlabel(u'Дата, декада', fontsize=16, color = 'k')
plt.ylabel(u'Высота снежного покрова, см', fontsize=16, color = 'k')
plt.grid(color='w')
plt.tick_params (pad = 5)
plt.xticks(color = 'k', rotation = 45)
plt.yticks(color = 'k', rotation = 0)
plt.savefig('C:/Python_script/Data_2017/Meteo_ru_field/Nadim/Analysis_1.png', format='png', dpi = 300, bbox_inches = 'tight')
plt.show
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_field'])
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_model'])
plt.show
 
plt.style.use('ggplot')
fig2 = plt.figure(figsize = (12,8))
ax2 = fig2.add_subplot(111)
ax2 = plt.bar(df_data_dvina.index, df_data_dvina['mean'], color = 'k', align = 'center')

#a#x1 = plt.streamplot(df_data_nadim['mean'], df_data_nadim.index, 'b^')
#adf_data_nadim.plot(x='mean', y = df_data_nadim.index, kind = 'scatter')
plt.title(u'Изменение высоты снежного покрова в бассейне р. Северная Двина ', fontsize=20, color = 'k')
plt.xlabel(u'Дата, декада', fontsize=16, color = 'k')
plt.ylabel(u'Высота снежного покрова, см', fontsize=16, color = 'k')
plt.grid(color='w')
plt.tick_params (pad = 5)
plt.xticks(color = 'k', rotation = 45)
plt.yticks(color = 'k', rotation = 0)
plt.savefig('C:/Python_script/Data_2017/Meteo_ru_field/Nadim/Analysis_2.png', format='png', dpi = 300, bbox_inches = 'tight')
plt.show
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_field'])
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_model'])
plt.show

plt.style.use('ggplot')
fig3 = plt.figure(figsize = (12,8))
ax3 = fig3.add_subplot(111)
ax3 = plt.bar(df_data_oka.index, df_data_oka['mean'], color = 'k', align = 'center')

#a#x1 = plt.streamplot(df_data_nadim['mean'], df_data_nadim.index, 'b^')
#adf_data_nadim.plot(x='mean', y = df_data_nadim.index, kind = 'scatter')
plt.title(u'Изменение высоты снежного покрова в бассейне р. Ока ', fontsize=20, color = 'k')
plt.xlabel(u'Дата, декада', fontsize=16, color = 'k')
plt.ylabel(u'Высота снежного покрова, см', fontsize=16, color = 'k')
plt.grid(color='w')
plt.tick_params (pad = 5)
plt.xticks(color = 'k', rotation = 45)
plt.yticks(color = 'k', rotation = 0)
plt.savefig('C:/Python_script/Data_2017/Meteo_ru_field/Nadim/Analysis_3.png', format='png', dpi = 300, bbox_inches = 'tight')
plt.show
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_field'])
#ax1 =plt.plot(df_super_snow.index, df_super_snow['SWE_model'])
plt.show
