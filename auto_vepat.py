import pathlib
import os, sys
import numpy as np
import pandas as pd
import math
from openpyxl import load_workbook
import utils_vepat as utiv
import pcal_vepat as pcals

#dirDat = pathlib.Path('/home/sapthala/Projects19_20/VEPAT/From_Natalia')
"""
configure this according to the input data maybe store as a dataframe

utive.excel_vpat(dirDat/'path the input datafram')

d ={'Person': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    'Best guess': [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3],
    'Min': [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05],
    'Max': [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]}
"""
########Elicitation inputs###
elc = int(input("Elecitation: "))
du = 4
print("Duration:", du)

################

#create table based on the inputs
df1 = utiv.table_vpt('pNo', 'bestG', 'Best_guessR', 'minG', 'maxG')

#calculate stats based on the table
df2 = utiv.table_stat_vpt(df1)

#calculations for plotting and other, calculations from this function saved as a dictionary
erp_cals = utiv.cal_vpt(df1,df2,elc,du)

#Table: Near Vent Processes
near_vent = utiv.table_near_vent_proc(erp_cals)

# P of death from one ballistics: tables & calculations
phit = pcals.risk_cal.from_input()
df1 = utiv.table_phit()
phit.load_dfs(df1, df2=None)

#Tables of Death from one ballistic: 0.2 m/0.3/0.4
phit_tbl = phit.phit_cal()

#ballistics 100m table for statnadrd, adjusted
df100 = utiv.ballistics_100m(erp_cals)
phit.load_dfs(df1, df100)
ball_100m = phit.ballis_cal()

#ballistics 350m table for statnadrd, adjusted
df350 = utiv.ballistics_350m(erp_cals)
phit.load_dfs(df1, df350)
ball_350m = phit.ballis_cal()


#ballistics 750m table for statnadrd, adjusted
df750 = utiv.ballistics_750m(erp_cals)
phit.load_dfs(df1, df750)
ball_750m = phit.ballis_cal()

