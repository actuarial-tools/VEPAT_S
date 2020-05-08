import pandas as pd
import volcano as vol
import whiteIsland as wht
import utils_vepat as utiv
import pcal_vepat as pcals
import whiteIsland as white
import ruapehu as ruphu



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

#get base paramters depening on the volcano
base_para = get_inps.base_para()
cal_type1 = base_para['calculation type'][0]
cal_type2 = base_para['calculation type'][1] #if no need to calcalate leave empty
cal_type3 = base_para['calculation type'][2] #if no need to calcalate leave empty

distance1 = base_para['Distance'][0]
distance2 = base_para['Distance'][1] #if no need to calcalate leave empty
distance3 = base_para['Distance'][2] #if no need to calcalate leave empty

site1 = base_para['Site location'][0]
site2 = base_para['Site location'][1] #if no need to calcalate leave empty
site3 = base_para['Site location'][2] #if no need to calcalate leave empty


#create table based on the inputs
#df0 = utiv.table_vpt('pNo', 'bestG', 'Best_guessR', 'minG', 'maxG')
df0 = get_inps.table_vpt()

#calculate stats based on the table
#get_inps.load_df(df0)
#df00 = get_inps.table_stat_vpt()
df00 =get_inps.table_stat_vpt()

#calculations for plotting and other, calculations from this function saved as a dictionaryx
erp_cals = get_inps.cal_vpt()

#Table: Near Vent Processes
near_vent = get_inps.table_near_vent_proc()

# P of death from one ballistics: tables & calculations
phit = pcals.PcalsVepat.from_input()
df1 = get_inps.table_phit()
phit.load_dfs(df1, df2=None)

#Tables of Death from one ballistic: 0.2 m/0.3/0.4
phit_tbl = phit.phit_cal()

#elecitation statistics plot
get_inps.elici_plot()


#do calculations based on thee volcano from here onwards
#df100, df350, df750 = get_inps.volcano_cals()


if confg == "config_whiteIsland.JSON":
    cng = white.white_island(du=du, elc=elc, eldate=eldate, filename=confg,
                             volcano=volcano)
    # generate ballistics dfs with initial input parameters
    df100, df350, df750 = cng.table_ballis()

    # ballistics 100m table for statnadrd, adjusted
    phit.load_dfs(df1, df100)
    ball_100m = phit.ballis_cal()

    # ballistics 350m table for statnadrd, adjusted
    phit.load_dfs(df1, df350)
    ball_350m = phit.ballis_cal()

    # ballistics 750m table for statnadrd, adjusted
    phit.load_dfs(df1, df750)
    ball_750m = phit.ballis_cal()

    #generate all the surge tables (9 tables)
    df_srg100strd, df_srg350strd, df_srg750strd, df_srg100adjc, df_srg350adjc, \
    df_srg750adjc, df_srg100adjh, df_srg350adjh, df_srg750adjh = cng.table_surge()

    ##risk of dying in an eruption (rde) calculations:
    # inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
    # cal_type1 calculation
    rde_100strd = cng.risk_dying_dicts(ball_100m, df_srg100strd, distance1, site1, cal_type1, df1=near_vent)
    rde_350strd = cng.risk_dying_dicts(ball_350m, df_srg350strd, distance2, site2, cal_type1, df1=None)
    rde_750strd = cng.risk_dying_dicts(ball_750m, df_srg750strd, distance3, site3, cal_type1, df1=None)

    # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR
    rde_100adjc = cng.risk_dying_dicts(ball_100m, df_srg100adjc, distance1, site1, cal_type2, df1=near_vent)
    rde_350adjc = cng.risk_dying_dicts(ball_350m, df_srg350adjc, distance2, site2, cal_type2, df1=None)
    rde_750adjc = cng.risk_dying_dicts(ball_750m, df_srg750adjc, distance3, site3, cal_type2, df1=None)

    # ADJUSTED - HELICOPTER IN SOUTHERN SECTOR
    rde_100adjh = cng.risk_dying_dicts(ball_100m, df_srg100adjh, distance1, site1, cal_type3, df1=near_vent)
    rde_350adjh = cng.risk_dying_dicts(ball_350m, df_srg350adjh, distance2, site2, cal_type3, df1=None)
    rde_750adjh = cng.risk_dying_dicts(ball_750m, df_srg750adjh, distance3, site3, cal_type3, df1=None)

    # generate summary tables and calculations
    pd.options.display.float_format = '{:.3g}'.format
    summary_strd, slope_strd, yincp_strd, cal_strd = cng.df_summary(erp_cals, rde_100strd, rde_350strd, rde_750strd, cal_type1)
    summary_adjc, slope_adjc, yincp_adjc, cal_adjc = cng.df_summary(erp_cals, rde_100adjc, rde_350adjc, rde_750adjc, cal_type2)
    summary_adjh, slope_adjh, yincp_adjh, cal_adjh = cng.df_summary(erp_cals, rde_100adjh, rde_350adjh, rde_750adjh, cal_type3)

    # generate volcano specific plots
    # risk summary plots
    cng.summary_plots(summary_strd, cal_type1)
    cng.summary_plots(summary_adjc, cal_type2)
    cng.summary_plots(summary_adjh, cal_type3)

    # Generate summary table with slopes, intercepts and calculation type

    tb_smry = {'cal type': [cal_type1, cal_type2, cal_type3],
               'slope': [slope_strd, slope_adjc, slope_adjh],
               'yinc': [yincp_strd, yincp_adjc, yincp_adjh]}
    df_smry = pd.DataFrame(data=tb_smry)

    # Generate final risk zone table
    riskzn = cng.riskzn(df_smry)

if confg == "config_ruapehu.JSON":
    cng = ruphu.ruapehu(du=du, elc=elc, eldate=eldate, filename=confg,
                        volcano=volcano)
    # generate ballistics dfs with initial input parameters
    df100, df350, df750 = cng.table_ballis()

    # ballistics 100m table for statnadrd, adjusted
    phit.load_dfs(df1, df100)
    ball_100m = phit.ballis_cal()

    # ballistics 350m table for statnadrd, adjusted
    phit.load_dfs(df1, df350)
    ball_350m = phit.ballis_cal()

    # ballistics 750m table for statnadrd, adjusted
    phit.load_dfs(df1, df750)
    ball_750m = phit.ballis_cal()

    #generate all the surge tables (9 tables)
    df_srg100strd, df_srg350strd, df_srg750strd = cng.table_surge()

    ##risk of dying in an eruption (rde) calculations:
    # inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
    # cal_type1 calculation
    rde_100strd = cng.risk_dying_dicts(ball_100m, df_srg100strd, distance1, site1, cal_type1, df1=near_vent)
    rde_350strd = cng.risk_dying_dicts(ball_350m, df_srg350strd, distance2, site2, cal_type1, df1=None)
    rde_750strd = cng.risk_dying_dicts(ball_750m, df_srg750strd, distance3, site3, cal_type1, df1=None)

    # generate summary tables and calculations
    pd.options.display.float_format = '{:.3g}'.format
    summary_strd, slope_strd, yincp_strd, cal_strd = cng.df_summary(erp_cals, rde_100strd, rde_350strd, rde_750strd, cal_type1)

    # generate volcano specific plots
    # risk summary plots
    cng.summary_plots(summary_strd, cal_type1)

    # Generate summary table with slopes, intercepts and calculation type

    tb_smry = {'cal type': [cal_type1],
               'slope': [slope_strd],
               'yinc': [yincp_strd]}
    df_smry = pd.DataFrame(data=tb_smry)

    # Generate final risk zone table
    riskzn = cng.riskzn(df_smry)



