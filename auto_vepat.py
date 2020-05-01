import pandas as pd
import volcano as vol
import whiteIsland as wht
import utils_vepat as utiv
import pcal_vepat as pcals


# Get Elicitation Inputs
volcano = input("Volcano:")
confg= input("Configuration file (JSON):") #config_whiteIsland.JSON
eldate= input("Elicitation date:")
print("Only enter one of Elicitation (days/s) or Duration (week/s), if non enter 0")

elc = int(input("Elicitation (day/s):"))
if elc > 0:
    du = 0
else:
    du = int(input("Duration (week/s):"))

# Get Elicitation Inputs:
get_inps = vol.volcano(elc, du, volcano, eldate, filename=confg)
inputs = get_inps.inp_para()


# Calculation types (This can be modified depebding the claculation types for different volcanoes)
cal_type1 = 'Standard'
cal_type2 = 'Adjusted for Crater floor' #if no need to calcalate leave empty
cal_type3 = 'Adjusted for Helicopter south. sector' #if no need to calcalate leave empty


#create table based on the inputs
#df0 = utiv.table_vpt('pNo', 'bestG', 'Best_guessR', 'minG', 'maxG')
df0 = get_inps.table_vpt()

#calculate stats based on the table
#get_inps.load_df(df0)
#df00 = get_inps.table_stat_vpt()
df00 =get_inps.table_stat_vpt()

#calculations for plotting and other, calculations from this function saved as a dictionaryx
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
#cal_type1 calculation
rde_100strd = utiv.risk_dying_dicts(ball_100m, df_srg100strd, 100, "Overlooking lake", cal_type1, df1 = near_vent)
rde_350strd = utiv.risk_dying_dicts(ball_350m, df_srg350strd, 350, "Fumerole 0", cal_type1, df1 = None)
rde_750strd = utiv.risk_dying_dicts(ball_750m, df_srg750strd, 750, "Factory", cal_type1, df1 = None)

#ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR
rde_100adjc = utiv.risk_dying_dicts(ball_100m, df_srg100adjc, 100, "Overlooking lake", cal_type2, df1 = near_vent)
rde_350adjc = utiv.risk_dying_dicts(ball_350m, df_srg350adjc, 350, "Fumerole 0", cal_type2, df1 = None)
rde_750adjc = utiv.risk_dying_dicts(ball_750m, df_srg750adjc, 750, "Factory", cal_type2, df1 = None)


#ADJUSTED - HELICOPTER IN SOUTHERN SECTOR
rde_100adjh = utiv.risk_dying_dicts(ball_100m, df_srg100adjh, 100, "Overlooking lake", cal_type3, df1 = near_vent)
rde_350adjh = utiv.risk_dying_dicts(ball_350m, df_srg350adjh, 350, "Fumerole 0", cal_type3, df1 = None)
rde_750adjh = utiv.risk_dying_dicts(ball_750m, df_srg750adjh, 750, "Factory", cal_type3, df1 = None)


#generate summary tables and calculations
pd.options.display.float_format = '{:.3g}'.format
summary_strd, slope_strd, yincp_strd, cal_strd = utiv.df_summary(erp_cals, rde_100strd, rde_350strd, rde_750strd, cal_type1)
summary_adjc, slope_adjc, yincp_adjc, cal_adjc = utiv.df_summary(erp_cals, rde_100adjc, rde_350adjc, rde_750adjc, cal_type2)
summary_adjh, slope_adjh, yincp_adjh, cal_adjh = utiv.df_summary(erp_cals, rde_100adjh, rde_350adjh, rde_750adjh, cal_type3)



#generate plots
#elecitation statistics plot
utiv.elici_plot(inputs, df0, df00)
#risk summary plots
utiv.summary_plots(summary_strd, inputs, cal_type1)
utiv.summary_plots(summary_adjc, inputs, cal_type2)
utiv.summary_plots(summary_adjh, inputs, cal_type3)



#Genrate summary table with slopes, intercepts and calculation type

tb_smry = {'cal type': [cal_strd, cal_adjc ,cal_adjh],
           'slope': [slope_strd, slope_adjc, slope_adjh],
            'yinc':[yincp_strd, yincp_adjc, yincp_adjh ]}
df_smry = pd.DataFrame(data=tb_smry)

#Generate final risk zone table
riskzn = utiv.riskzn(df_smry)
