"""Helper functions for VEPAT excel automation"""

import pandas as pd
import numpy as np
import math
# import pathlib
# import os, sys


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


###############calculating Pdeath from one ballistic##############
# initial table with ballistic information
def table_phit():
    ball_dia = [0.2, 0.3, 0.4]
    person_dia = [1, 1, 1]
    sq_lng = [30, 30, 30]

    d1 = {'Bdia': ball_dia,
          'Pdia': person_dia,
          'Sqln': sq_lng}
    db1 = pd.DataFrame(data=d1)

    return db1












