import pandas as pd
import volcano as vol
import whiteIsland as wht
import utils_vepat as utiv
import pcal_vepat as pcals
from whiteIsland import white_island
from ruapehu import ruapehu
from tongariro import tongariro
from ngauruhoe import ngauruhoe



# Get Elicitation Inputs
volcano = input("Volcano:")
confg= input("Configuration file (JSON):") #config_whiteIsland.JSON
eldate= input("Elicitation date:")
print("Only enter one of Elicitation Duration (days/s) or Elicitation Duration (week/s), if non enter 0")

elc = int(input("Elicitation Duration (day/s):"))
if elc > 0:
    du = 0
else:
    du = int(input("Elicitation Duration (week/s):"))

# Get Elicitation Inputs:
get_inps = vol.volcano(elc, du, volcano, eldate, filename=confg)
inputs = get_inps.inp_para()

#get base paramters depening on the volcano
base_para = get_inps.base_para()
cal_type1 = base_para['calculation type'][0]
cal_type2 = base_para['calculation type'][1] #if no need to calcalate leave empty
cal_type3 = base_para['calculation type'][2] #if no need to calcalate leave empty

distance1 = base_para['Distance'][0]
distance2 = base_para['Distance'][1]
distance3 = base_para['Distance'][2]


site1 = base_para['Site location'][0]
site2 = base_para['Site location'][1]
site3 = base_para['Site location'][2]



#create table based on the inputs
df0 = get_inps.table_vpt()
#df0000 = get_inps.table_vpt_last()

#calculate stats based on the table
df00 = get_inps.table_stat_vpt()
#df000 = get_inps.table_stat_vpt_last()

#do calculations based on thee volcano from here onwards

if confg == "config_whiteIsland.JSON":
    white = white_island(du=du, elc=elc, eldate=eldate, filename=confg,
                             volcano=volcano)

    white.doCalculationsPlots(pcals, get_inps, base_para, distance1, distance2, distance3,
                                site1, site2, site3, cal_type1, cal_type2, cal_type3)



if confg == "config_ruapehu.JSON":
    ruapehu = ruapehu(du=du, elc=elc, eldate=eldate, filename=confg,
                        volcano=volcano)
    ruapehu.doCalculationsPlots(pcals, get_inps, base_para, distance1, distance2, distance3,
                                  site1, site2, site3, cal_type1)



if confg == "config_tongariro.JSON":
    tongariro = tongariro(du=du, elc=elc, eldate=eldate, filename=confg,
                        volcano=volcano)

    tongariro.doCalculationsPlots(pcals, get_inps, distance1, distance2, site1, site2, cal_type1)

if confg == "config_ngauruhoe.JSON":
    ngauruhoe = ngauruhoe(du=du, elc=elc, eldate=eldate, filename=confg,
                        volcano=volcano)
    ngauruhoe.doCalculationsPlots(pcals, get_inps, base_para, distance1, distance2, distance3,
                                  site1, site2, site3, cal_type1)



