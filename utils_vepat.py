"""Helper functions for VEPAT excel automation"""

import pandas as pd
import numpy as np
import math
# import pathlib
# import os, sys


#create table based on the inputs
def table_vpt(pNo, bestG, minG, maxG):

    
    d1 ={'Person': pNo, 
        'Best guess': bestG,
        'Min': minG,
        'Max': maxG}
    dfd = pd.DataFrame(data = d1)
    dfd['Error low'] = dfd['Best guess'] - dfd['Min']
    dfd['Error high'] = dfd['Max'] - dfd['Best guess']
    
    return dfd

#calculate stats based on the table

def table_stat_vpt(dfd):
    mean_bestG = dfd['Best guess'].mean()
    median_bestG = dfd['Best guess'].median()
    #qntl_bestG = dfd['Best guess'].quantile(0.84) #84th percentile
    pcntl_bestG = np.percentile(dfd['Best guess'].values, 84)
    
    mean_min = dfd['Min'].mean()
    median_min = dfd['Min'].median()

    mean_max = dfd['Max'].mean()
    median_max = dfd['Max'].median()

    d2 = {'Stat': ['Mean', 'Median', '84th percentile'],
         'Best Guess': [mean_bestG, median_bestG, pcntl_bestG ],
         'Min': [mean_min, median_min, ""], 
         'Max': [mean_max, median_max, ""]}
    d1_stat = pd.DataFrame(data = d2)
    return d1_stat
   
#calculations necessary to produce tables and plots   
#input parameters: dfd, d1_stat, elcitation, duration 
def cal_vpt(df2,elc,du):
    p_erup = df2.iloc[2]['Best Guess'] #P(eruption in period):
    p_Nerup = 1 - p_erup #P(no erupt. in period):
    
    if elc > 0:
        B6 = elc
    else:
        if du > 0:
            B6 = du*7
        else:
            B6 = -1
            
    if B6 > 0:
        B7 = B6*24 #days
    else:
        B7 = -1 #hours

    p_Neruphr = round(math.pow(p_Nerup, 1/B7), 3)
    
        
    erp_cls = {
              "P(eruption in period)": p_erup, 
              "P(no erupt. in period)": p_Nerup,
              "P(no eruption in hr)": p_Neruphr
 
    }
               
    return erp_cls

    
    
    #p_Neruphr = math.pow(p_Nerup, con1) 
    
    
    
    #p_eruphr = 

    
   
    
    

        
    
        
        
       