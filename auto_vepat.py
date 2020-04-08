import pathlib
import os, sys
import numpy as np
import pandas as pd
import math
from openpyxl import load_workbook
import utils_vepat as utiv
import pcal_vepat as pcals


# Get Elicitation Inputs
volcano = input("Volcano:")
eldate= input("Elicitation date:")
print("Only enter one of Elicitation (days/s) or Duration (week/s), if non enter 0")

elc = int(input("Elicitation (day/s):"))
if elc > 0:
    du = 0
else:
    du = int(input("Duration (week/s):"))

# Get Elicitation Inputs:
get_inps = utiv.inputs(elc, du, volcano, eldate)
inputs = get_inps.inp_para()


#create table based on the inputs
df0 = utiv.table_vpt('pNo', 'bestG', 'Best_guessR', 'minG', 'maxG')

#calculate stats based on the table
df00 = utiv.table_stat_vpt(df0)

#calculations for plotting and other, calculations from this function saved as a dictionary
erp_cals = utiv.cal_vpt(df00,elc,du)

# P of death from one ballistics: tables & calculations
phit = pcals.risk_cal.from_input()
df1 = utiv.table_phit()
phit.load_dfs(df1, df2=None)

#Table: Near Vent Processes
near_vent = utiv.table_near_vent_proc(erp_cals)

#Tables of Death from one ballistic: 0.2 m/0.3/0.4
phit_tbl = phit.phit_cal()

#generate ballistics dfs with initial input parameters
df100, df350, df750 = utiv.table_ballis(erp_cals)

#ballistics 100m table for statnadrd, adjusted
phit.load_dfs(df1, df100)
ball_100m = phit.ballis_cal()

#ballistics 350m table for statnadrd, adjusted
phit.load_dfs(df1, df350)
ball_350m = phit.ballis_cal()

#ballistics 750m table for statnadrd, adjusted
phit.load_dfs(df1, df750)
ball_750m = phit.ballis_cal()

#generate all the surge tables (9 tables)
df_srg100strd, df_srg350strd, df_srg750strd, df_srg100adjc, df_srg350adjc, \
df_srg750adjc, df_srg100adjh, df_srg350adjh, df_srg750adjh = utiv.table_surge(erp_cals)

##risk of dying in an eruption (rde) calculations:
#inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
#Standard calculation
rde_100strd = utiv.risk_dying_dicts(ball_100m, df_srg100strd, 100, "Overlooking lake", 'Standard Calculation', df1 = near_vent)
rde_350strd = utiv.risk_dying_dicts(ball_350m, df_srg350strd, 350, "Fumerole 0", 'Standard Calculation', df1 = None)
rde_750strd = utiv.risk_dying_dicts(ball_750m, df_srg750strd, 750, "Factory", 'Standard Calculation', df1 = None)

#ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR
rde_100adjc = utiv.risk_dying_dicts(ball_100m, df_srg100adjc, 100, "Overlooking lake", 'Standard Calculation', df1 = near_vent)
rde_350adjc = utiv.risk_dying_dicts(ball_350m, df_srg350adjc, 350, "Fumerole 0", 'Standard Calculation', df1 = None)
rde_750adjc = utiv.risk_dying_dicts(ball_750m, df_srg750adjc, 750, "Factory", 'Standard Calculation', df1 = None)


#ADJUSTED - HELICOPTER IN SOUTHERN SECTOR
rde_100adjh = utiv.risk_dying_dicts(ball_100m, df_srg100adjh, 100, "Overlooking lake", 'Standard Calculation', df1 = near_vent)
rde_350adjh = utiv.risk_dying_dicts(ball_350m, df_srg350adjh, 350, "Fumerole 0", 'Standard Calculation', df1 = None)
rde_750adjh = utiv.risk_dying_dicts(ball_750m, df_srg750adjh, 750, "Factory", 'Standard Calculation', df1 = None)





