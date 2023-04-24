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

import os


def cleah_history(pout:str):
    '''
    Task: Очистка результатов предыдушей работы скрипта

    Input parameters:
    pout : Input data path

    Returns: None (Clean folder)
    '''
    dirs_pout = os.listdir(pout)
    for file in dirs_pout:
        os.remove(pout + file)

# 2. Function --> makefolder
def makefolder(path:str) -> tuple[str]:
    '''
    Task: Check and create folder

    Parameters
    ----------
    path : Path to the folder.

    Returns
    -------
    path_OUT : New path for output data
    '''
    # Create folder for output data
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path