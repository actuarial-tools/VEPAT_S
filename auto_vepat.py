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
df0 = get_inps.table_vpt()

#calculate stats based on the table
df00 = get_inps.table_stat_vpt()


#do calculations based on thee volcano from here onwards

if confg == "config_whiteIsland.JSON":
    cng = white.white_island(du=du, elc=elc, eldate=eldate, filename=confg,
                             volcano=volcano)

    # calculations for plotting and other, calculations from this function saved as a dictionaryx
    erp_cals = cng.cal_vpt()

    # Table: Near Vent Processes
    near_vent = cng.table_near_vent_proc()

    # P of death from one ballistics: tables & calculations
    phit = pcals.PcalsVepat.from_input()
    df1 = get_inps.table_phit()
    phit.load_dfs(df1, df2=None)

    # Tables of Death from one ballistic: 0.2 m/0.3/0.4
    phit_tbl = phit.phit_cal()

    # elecitation statistics plot
    get_inps.elici_plot()


    # generate ballistics dfs with initial input parameters
    df_dis1, df_dis2, df_dis3 = cng.table_ballis()

    # ballistics 100m table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis1)
    ball_dis1 = phit.ballis_cal()

    # ballistics 350m table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis2)
    ball_dis2 = phit.ballis_cal()

    # ballistics 750m table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis3)
    ball_dis3 = phit.ballis_cal()

    #generate all the surge tables (9 tables)
    df_srgDis1strd, df_srgDis2strd, df_srgDis3strd, df_srgDis1adjc, df_srgDis2adjc, \
    df_srgDis3adjc, df_srgDis1adjh, df_srgDis2adjh, df_srgDis3adjh = cng.table_surge()

    ##risk of dying in an eruption (rde) calculations:
    # inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
    # cal_type1 calculation
    rde_Dis1strd = cng.risk_dying_dicts(ball_dis1, df_srgDis1strd, distance1, site1, cal_type1, df1=near_vent)
    rde_Dis2strd = cng.risk_dying_dicts(ball_dis2, df_srgDis2strd, distance2, site2, cal_type1, df1=None)
    rde_Dis3strd = cng.risk_dying_dicts(ball_dis3, df_srgDis3strd, distance3, site3, cal_type1, df1=None)

    # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR
    rde_Dis1adjc = cng.risk_dying_dicts(ball_dis1, df_srgDis1adjc, distance1, site1, cal_type2, df1=near_vent)
    rde_Dis2adjc = cng.risk_dying_dicts(ball_dis2, df_srgDis2adjc, distance2, site2, cal_type2, df1=None)
    rde_Dis3adjc = cng.risk_dying_dicts(ball_dis3, df_srgDis3adjc, distance3, site3, cal_type2, df1=None)

    # ADJUSTED - HELICOPTER IN SOUTHERN SECTOR
    rde_Dis1adjh = cng.risk_dying_dicts(ball_dis1, df_srgDis1adjh, distance1, site1, cal_type3, df1=near_vent)
    rde_Dis2adjh = cng.risk_dying_dicts(ball_dis2, df_srgDis2adjh, distance2, site2, cal_type3, df1=None)
    rde_Dis3adjh = cng.risk_dying_dicts(ball_dis3, df_srgDis3adjh, distance3, site3, cal_type3, df1=None)

    # generate summary tables and calculations
    pd.options.display.float_format = '{:.3g}'.format
    summary_strd, slope_strd, yincp_strd, cal_strd = cng.df_summary(erp_cals, rde_Dis1strd, rde_Dis2strd, rde_Dis3strd, cal_type1)
    summary_adjc, slope_adjc, yincp_adjc, cal_adjc = cng.df_summary(erp_cals, rde_Dis1adjc, rde_Dis2adjc, rde_Dis3adjc, cal_type2)
    summary_adjh, slope_adjh, yincp_adjh, cal_adjh = cng.df_summary(erp_cals, rde_Dis1adjh, rde_Dis2adjh, rde_Dis3adjh, cal_type3)

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

    # calculations for plotting and other, calculations from this function saved as a dictionaryx
    erp_cals = cng.cal_vpt()

    # Table: Near Vent Processes
    near_vent = cng.table_near_vent_proc()

    # P of death from one ballistics: tables & calculations
    phit = pcals.PcalsVepat.from_input()
    df1 = get_inps.table_phit()
    phit.load_dfs(df1, df2=None)

    # Tables of Death from one ballistic: 0.2 m/0.3/0.4
    phit_tbl = phit.phit_cal()

    # elecitation statistics plot
    get_inps.elici_plot()

 # generate ballistics dfs with initial input parameters
    df_dis1, df_dis2, df_dis3, df_dis4 = cng.table_ballis()

    # ballistics 0km table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis1)
    ball_dis1 = phit.ballis_cal()

    # ballistics 0.5km table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis2)
    ball_dis2 = phit.ballis_cal()

    # ballistics 1.3.km table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis3)
    ball_dis3 = phit.ballis_cal()

    # ballistics 1.3.km table for statnadrd, adjusted
    phit.load_dfs(df1, df_dis4)
    ball_dis4 = phit.ballis_cal()

    #generate all the surge tables (9 tables)
    df_srgDis1strd, df_srgDis2strd, df_srgDis3strd, df_srgDis4strd  = cng.table_surge()

    ##risk of dying in an eruption (rde) calculations:
    # inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
    # cal_type1 calculation
    rde_Dis1strd = cng.risk_dying_dicts(ball_dis1, df_srgDis1strd, distance1, site1, cal_type1, df1=near_vent)
    rde_Dis2strd = cng.risk_dying_dicts(ball_dis2, df_srgDis2strd, distance2, site2, cal_type1, df1=None)
    rde_Dis3strd = cng.risk_dying_dicts(ball_dis3, df_srgDis3strd, distance3, site3, cal_type1, df1=None)

    # generate summary tables and calculations
    pd.options.display.float_format = '{:.3g}'.format
    summary_strd, slope_strd, yincp_strd, cal_strd = cng.df_summary(erp_cals, rde_Dis1strd, rde_Dis2strd, rde_Dis3strd, cal_type1)

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



