"""Helper functions for VEPAT excel automation"""

import pandas as pd
import numpy as np
import math
# import pathlib
# import os, sys
import pcal_vepat as pcals


#create table based on the inputs
def table_vpt(pNo, bestG, Best_guessR, minG, maxG):
    pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
    Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
    minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
    maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

    d1 = {'Person': pNo,
          'Best guess': bestG,
          'Best guess rep': Best_guessR,
          'Min': minG,
          'Max': maxG}
    dfd = pd.DataFrame(data=d1)
    dfd['Error low'] = dfd['Best guess'] - dfd['Min']
    dfd['Error high'] = dfd['Max'] - dfd['Best guess']

    return dfd

#calculate stats based on the table

def table_stat_vpt(dfd):
    mean_bestG = dfd['Best guess'].mean()
    median_bestG = dfd['Best guess'].median()
    # qntl_bestG = dfd['Best guess'].quantile(0.84) #84th percentile
    # 84th percentile calculation over a range of columns:
    dfd84 = pd.concat(dfd[c] for c in ['Best guess', 'Best guess rep', 'Min', 'Max']).reset_index(drop=True)
    pcntl_bestG = np.percentile(dfd84.values, 84)

    mean_min = dfd['Min'].mean()
    median_min = dfd['Min'].median()

    mean_max = dfd['Max'].mean()
    median_max = dfd['Max'].median()

    d2 = {'Stat': ['Mean', 'Median', '84th percentile'],
          'Best Guess': [mean_bestG, median_bestG, pcntl_bestG],
          'Min': [mean_min, median_min, ""],
          'Max': [mean_max, median_max, ""]}
    d1_stat = pd.DataFrame(data=d2)
    return d1_stat
   
#calculations necessary to produce tables and plots   
#input parameters: dfd, d1_stat, elcitation, duration 
def cal_vpt(df1, df2, elc, du):
    p_erup = df2.iloc[2]['Best Guess']  # P(eruption in period):
    p_Nerup = 1 - p_erup  # P(no erupt. in period):

    if elc > 0:
        B6 = elc
    else:
        if du > 0:
            B6 = du * 7
        else:
            B6 = -1

    if B6 > 0:
        B7 = B6 * 24  # days
    else:
        B7 = -1  # hours

    p_Neruphr = math.pow(p_Nerup, 1 / B7)
    p_eruphr = 1 - p_Neruphr
    p_lrgeruphr = p_eruphr / 100
    p_mderuphr = (p_eruphr / 10) - p_lrgeruphr
    p_smleruphr = p_eruphr - p_mderuphr - p_lrgeruphr


    erp_cls = {
        "P(eruption in period)": p_erup,
              "P(no erupt. in period)": p_Nerup,
              "P(no eruption in hr)": round(p_Neruphr, 3),
              "P(eruption in hr)": round(p_eruphr, 4),
              "P(small eruption in hr)": round(p_smleruphr, 4),
              "P(moderate eruption in hr)": round(p_mderuphr,5),
              "P(large eruption in hr)": round(p_lrgeruphr,6)
    }

    return erp_cls


###############tables involve with total risk of dying in hour##############
# initial table with ballistic information, this is used by pcal_vepat for calculating probability of hit
def table_phit():
    ball_dia = [0.2, 0.3, 0.4]
    person_dia = [1, 1, 1]
    sq_lng = [30, 30, 30]

    d1 = {'Bdia': ball_dia,
          'Pdia': person_dia,
          'Sqln': sq_lng}
    df1 = pd.DataFrame(data=d1)

    return df1

#function to extract values from dictionary: erp_cls
def get_p_hourly(dct1):
    #getting P(hourly) from erp_cls
    p_small = dct1.get("P(small eruption in hr)", "")
    p_mod = dct1.get("P(moderate eruption in hr)", "")
    p_lrg = dct1.get("P(large eruption in hr)", "")
    return p_small, p_mod, p_lrg

def tbl_surge(dct1,lst1,lst2,lst3):
    tb1 = {'Eruption size': dct1,
                  'P(hourly)': lst1,
                  'P(given eruption, exposure to surge)': lst2,
                  'P(given exposure, death from surge)': lst3}
    tb1_p = pd.DataFrame(data=tb1)
    tb1_p['P(given eruption, death from surge)'] = tb1_p['P(given eruption, exposure to surge)'] * tb1_p['P(given exposure, death from surge)']
    tb1_p['P(death from surge in hr)'] = tb1_p['P(hourly)'] * tb1_p['P(given eruption, death from surge)']

    return tb1_p



#create table: NEAR VENT PROCESSES (WATER SPOUTS, LANDSLIDES, SHOCK/PRESSURE WAVES, DENSE SLUGS, ETC.)
#the same table is used for in the Standard calculation, ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR, and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR

def table_near_vent_proc(dct1):
    #getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small","Moderate","Large"]
    p_hrly = [p_small, p_mod, p_lrg]
    p_erp_expo = [0, 0.1, 1]
    p_exo_death = [0.9, 0.9, 1]

    df_nvp = {'Eruption size': erps,
              'P(hourly)': p_hrly,
              'P(given eruption, exposure to near vent processes)': p_erp_expo,
              'P(given exposure, death from near vent processes)': p_exo_death}
    table_nvp = pd.DataFrame(data=df_nvp)
    table_nvp['P(given eruption, death from near vent processes)'] = table_nvp[ 'P(given eruption, exposure to near vent processes)'] * table_nvp['P(given exposure, death from near vent processes)']
    table_nvp['P(death from near vent processes in hr)'] = table_nvp['P(hourly)'] * table_nvp['P(given eruption, death from near vent processes)']

    return table_nvp


#Generate table for Ballistics, need 3 different tables for Distance = 100 m/350 m and 750 m
#100m
def ballistics_100m(dct1):
    # getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small", "Moderate", "Large"]
    p_hrly = [p_small, p_mod, p_lrg]
    ball_dia = [0.3, 0.3, 0.3]
    ball_area = [5, 50, 200]

    ## p_erp_death_ball = [x, y, z]

    df2_ballp100 = {'Eruption size': erps,
                    'P(hourly)': p_hrly,
                    'Ballistic diameter (m)': ball_dia,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': ball_area, }
    # 'P(given eruption, death from ballistics)': p_erp_death_ball}
    df2_bp100 = pd.DataFrame(data=df2_ballp100)
    return df2_bp100
#350m
def ballistics_350m(dct1):
    # getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small", "Moderate", "Large"]
    p_hrly = [p_small, p_mod, p_lrg]
    ball_dia = [0.2, 0.3, 0.3]
    ball_area = [0.1, 10, 100]

    ## p_erp_death_ball = [x, y, z]

    df2_ballp350 = {'Eruption size': erps,
                    'P(hourly)': p_hrly,
                    'Ballistic diameter (m)': ball_dia,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': ball_area, }
    # 'P(given eruption, death from ballistics)': p_erp_death_ball}
    df2_bp350 = pd.DataFrame(data=df2_ballp350)
    return df2_bp350

def ballistics_750m(dct1):
    # getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small", "Moderate", "Large"]
    p_hrly = [p_small, p_mod, p_lrg]
    ball_dia = [0, 0.2, 0.3]
    ball_area = [0, 5, 10]

    ## p_erp_death_ball = [x, y, z]

    df2_ballp750 = {'Eruption size': erps,
                    'P(hourly)': p_hrly,
                    'Ballistic diameter (m)': ball_dia,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': ball_area, }
    # 'P(given eruption, death from ballistics)': p_erp_death_ball}
    df2_bp750 = pd.DataFrame(data=df2_ballp750)
    return df2_bp750

#SURGE: 100m/350m/750m/ for standard, adjusted crator floor and helicopter in southern sector

def table_surge(dct1):
    #getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small","Moderate","Large"]
    p_hrly = [p_small, p_mod, p_lrg]

    #P(given eruption, exposure to surge) at 100, 350 and 750m distance for STANDARD CALCULATION (strd),
    #ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR (adjc) and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR (adjh)
    #strd
    p_erp_expo100_strd = [0.01, 0.3, 0.4]
    p_erp_expo350_strd = [0, 0.3, 0.4]
    p_erp_expo750_strd = [0, 0.2, 0.4]
    #adjc
    p_erp_expo100_adjc = [1, 1, 1]
    p_erp_expo350_adjc = [0.5, 1, 1]
    p_erp_expo750_adjc = [0, 1, 1]
    #adjh
    p_erp_expo100_adjh = [1, 1, 1]
    p_erp_expo350_adjh = [0, 0.3, 1]
    p_erp_expo750_adjh = [0, 0.05, 1]

   #P(given exposure, death from surge) at 100m, 350m and 750m distances
    p_exo_death100 = [0.95, 1, 1]
    p_exo_death350 = [0.95, 0.95, 1]
    p_exo_death750= [0.95, 0.95, 0.95]

    #generate all 9 tables:
    df1_srg100strd = tbl_surge(erps, p_hrly, p_erp_expo100_strd, p_exo_death100)
    df1_srg350strd = tbl_surge(erps, p_hrly, p_erp_expo350_strd, p_exo_death350)
    df1_srg750strd = tbl_surge(erps, p_hrly, p_erp_expo750_strd, p_exo_death750)

    df1_srg100adjc = tbl_surge(erps, p_hrly, p_erp_expo100_adjc, p_exo_death100)
    df1_srg350adjc = tbl_surge(erps, p_hrly, p_erp_expo350_adjc, p_exo_death350)
    df1_srg750adjc = tbl_surge(erps, p_hrly, p_erp_expo750_adjc, p_exo_death750)

    df1_srg100adjh = tbl_surge(erps, p_hrly, p_erp_expo100_adjh, p_exo_death100)
    df1_srg350adjh = tbl_surge(erps, p_hrly, p_erp_expo350_adjh, p_exo_death350)
    df1_srg750adjh = tbl_surge(erps, p_hrly, p_erp_expo750_adjh, p_exo_death750)

    return df1_srg100strd, df1_srg350strd, df1_srg750strd, df1_srg100adjc, df1_srg350adjc, df1_srg750adjc, df1_srg100adjh, df1_srg350adjh, df1_srg750adjh




