# -*- coding: utf-8 -*-
"""
Description: Reading COSMO verification results calculated based on script created
             by Denis Blinov

Authors: Evgenii Churiulin,

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    28.09.2016 Evgenii Churiulin, RHMS
           Initial release
    1.2    26.04.2023 Evgenii Churiulin, MPI-BGC
           Prepared version v2.0
"""

# =============================     Import modules     ====================
import pandas as pd
# =============================   Personal functions   ====================
def get_data(path:str):
    # Read txt data!
    return pd.read_csv(path, comment ='#', sep = '\t')
# ================   User settings (have to be adapted)  ==================

# Input path:
main = 'D:/Churyulin/msu_cosmo/forecast/verif_northDvina4Zhenya/txt'

# Common input names for statistical parameters:
fname = 'vf_se_cm07etr_oper'       # verification results
ename = 'stat_error_cm07etr_oper'  # precipitation errors

# Time periods:
winter = '2017120100_2018022821'
spring = '2018030100_2018053121'
summer = '2018060100_2018083121'

# -- Files with statistic parameter calculated based on COSMO data:
stat_files = {
    # Statistic by T2m
    't2m' : [f'{fname}_t2m_{winter}.txt',
             f'{fname}_t2m_{spring}.txt',
             f'{fname}_t2m_{summer}.txt',
    ],
    # Statistic by Td2m
    'td2m': [f'{fname}_td2m_{winter}.txt',
             f'{fname}_td2m_{spring}.txt',
             f'{fname}_td2m_{summer}.txt',
    ],
    # Statistic by precipitations (point, radius 15 km, radius 30 km)
    'prec': [f'{fname}_TOT_PREC_{winter}.txt',
             f'{fname}_TOT_PREC_{spring}.txt',
             f'{fname}_TOT_PREC_{summer}.txt',
             f'{fname}_TOT_PREC_av15km_{winter}.txt',
             f'{fname}_TOT_PREC_av15km_{spring}.txt',
             f'{fname}_TOT_PREC_av15km_{summer}.txt',
             f'{fname}_TOT_PREC_mx30km_{winter}.txt',
             f'{fname}_TOT_PREC_mx30km_{spring}.txt',
             f'{fname}_TOT_PREC_mx30km_{summer}.txt',
    ],
    # Statistic by precipitations errors (point, radius 15 km, radius 30 km)
    'eprec': [f'{ename}_TOT_PREC_{winter}.txt',
              f'{ename}_TOT_PREC_{spring}.txt',
              f'{ename}_TOT_PREC_{summer}.txt',
              f'{ename}_TOT_PREC_av15km_{winter}.txt',
              f'{ename}_TOT_PREC_av15km_{spring}.txt',
              f'{ename}_TOT_PREC_av15km_{summer}.txt',
              f'{ename}_TOT_PREC_mx30km_{winter}.txt',
              f'{ename}_TOT_PREC_mx30km_{spring}.txt',
              f'{ename}_TOT_PREC_mx30km_{summer}.txt',
    ],
}
#=============================    Main program   ==============================
if __name__ == '__main__':
    # Create lists for parameters:
    t2m_data = []
    td2m_data = []
    prec_data = []
    eprec_data = []
    
    # Get T2m data from COSMO forecasts!
    for file in stat_files.get('t2m'):
        t2m_data.append(get_data(main + f'/{file}'))
    # Get dew point data from COSMO forecasts!
    for path in stat_files.get('td2m'):
        td2m_data.append(get_data(main + f'/{file}'))
    # Get precipitation data
    for path in stat_files.get('prec'):
        prec_data.append(get_data(main + f'/{file}'))
    # Get precipitation data (errors)
    for path in stat_files.get('eprec'):
        eprec_data.append(get_data(main + f'/{file}'))
#=============================    End of program   ============================
