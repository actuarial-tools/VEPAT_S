"""Helper functions for VEPAT excel automation"""

import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go


# class inputs(object):
#     def __init__(self, el, du):
#         self.el = el
#         self.du = du
#
#
#     def check_inputs(self):
#         if self.el > 0:
#            print('')
#
#     @classmethod
#     def from_input(cls):
#         return cls(
#             print("Only enter one of Elicitation (days/s) or Duration (week/s):"),
#             int(input("Elicitation (day/s):")),
#
#             int(input("Duration (week/s):")),
#         )

# Generate dictionary from the elicitation parameters
class inputs:
    def __init__(self, elc, du, volcano, eldate):
        self.elc = elc
        self.du = du
        self.volcano = volcano
        self.eldate = eldate

    def inp_para(self):
        inps = {
            "Volcano": self.volcano,
            "Elicitation date": self.eldate,
            "Elicitation (day/s)": self.elc,
            "duration (week/s)": self.du
        }

        return inps


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
def cal_vpt(df2, elc, du):
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
              "P(no eruption in hr)": float(format(p_Neruphr, '.6g')), # format(val, '.6g') => give 6 significant digits
              "P(eruption in hr)": float(format(p_eruphr, '.6g')),
              "P(small eruption in hr)": float(format(p_smleruphr, '.6g')),
              "P(moderate eruption in hr)": float(format(p_mderuphr, '.6g')),
              "P(large eruption in hr)": float(format(p_lrgeruphr, '.6g'))
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


def tbl_ballis(dct1,lst1,lst2,lst3):
    df_ballp = {'Eruption size': dct1,
                    'P(hourly)': lst1,
                    'Ballistic diameter (m)': lst2,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': lst3}
    # 'P(given eruption, death from ballistics)': p_erp_death_ball}
    df_bp = pd.DataFrame(data=df_ballp)
    return df_bp

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
def table_ballis(dct1):
    # getting P(hourly) from erp_cls
    p_small = get_p_hourly(dct1)[0]
    p_mod = get_p_hourly(dct1)[1]
    p_lrg = get_p_hourly(dct1)[2]

    erps = ["Small", "Moderate", "Large"]
    p_hrly = [p_small, p_mod, p_lrg]

    #Ballistic diameter (m)
    ball_dia100 = [0.3, 0.3, 0.3]
    ball_dia350 = [0.2, 0.3, 0.3]
    ball_dia750 = [0, 0.2, 0.3]

   #Given eruption, # ballistics in reference area
    ball_area100 = [5, 50, 200]
    ball_area350 = [0.1, 10, 100]
    ball_area750 = [0, 5, 10]

    df_ballis100 = tbl_ballis(erps, p_hrly, ball_dia100, ball_area100)
    df_ballis350 = tbl_ballis(erps, p_hrly, ball_dia350, ball_area350)
    df_ballis750 = tbl_ballis(erps, p_hrly, ball_dia750, ball_area750)

    return df_ballis100, df_ballis350, df_ballis750


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
    df_srg100strd = tbl_surge(erps, p_hrly, p_erp_expo100_strd, p_exo_death100)
    df_srg350strd = tbl_surge(erps, p_hrly, p_erp_expo350_strd, p_exo_death350)
    df_srg750strd = tbl_surge(erps, p_hrly, p_erp_expo750_strd, p_exo_death750)

    df_srg100adjc = tbl_surge(erps, p_hrly, p_erp_expo100_adjc, p_exo_death100)
    df_srg350adjc = tbl_surge(erps, p_hrly, p_erp_expo350_adjc, p_exo_death350)
    df_srg750adjc = tbl_surge(erps, p_hrly, p_erp_expo750_adjc, p_exo_death750)

    df_srg100adjh = tbl_surge(erps, p_hrly, p_erp_expo100_adjh, p_exo_death100)
    df_srg350adjh = tbl_surge(erps, p_hrly, p_erp_expo350_adjh, p_exo_death350)
    df_srg750adjh = tbl_surge(erps, p_hrly, p_erp_expo750_adjh, p_exo_death750)

    return df_srg100strd, df_srg350strd, df_srg750strd, df_srg100adjc, df_srg350adjc, df_srg750adjc, df_srg100adjh, df_srg350adjh, df_srg750adjh


def risk_dying_cal(df2, df3, df1, val):
    if isinstance(df1, pd.DataFrame): #check if the dataframe is None or not
        val1 = df2.iloc[val]['P(hourly)']
        val2 = df1.iloc[val]['P(given eruption, death from near vent processes)']
        val3 = df2.iloc[val]['P(given eruption, death from ballistics)']
        val4 = df3.iloc[val]['P(given eruption, death from surge)']
        RDE = val1 * (1 - (1 - val2) * (1 - val3) * (1 - val4))  # risk of dying from eruption
    else:
        val1 = df2.iloc[val]['P(hourly)']
        val3 = df2.iloc[val]['P(given eruption, death from ballistics)']
        val4 = df3.iloc[val]['P(given eruption, death from surge)']
        RDE = val1 * (1 - (1 - val3) * (1 - val4))  # risk of dying from eruption
    return RDE




def risk_dying_dicts(df2, df3, dis, obsp, calt, df1): #here dis = distance = 100, 350, 750m depending on the input dfs/ obps: observation point/calt = calculation type
    for i in 0, 1, 2:
        if i == 0:
            RDE_sml = risk_dying_cal(df2, df3, df1, val = i)
        elif i == 1:
            RDE_med = risk_dying_cal(df2, df3, df1, val = i)
        else:
            RDE_lrg = risk_dying_cal(df2, df3, df1, val = i)

    TRDE = RDE_sml + RDE_med + RDE_lrg   #total risk of dying in hour

    RDE = {
        "Calculation:": calt,
        "Distance(m):": dis,
        "Site description:": obsp,
        "Total risk dying in hour:": float(format(TRDE, '.3g')),
        "Risk dying from small eruption in hour:": float(format(RDE_sml, '.3g')),
        "Risk dying from moderate eruption in hour:": float(format(RDE_med, '.3g')),
        "Risk dying from large eruption in hour:": float(format(RDE_lrg, '.3g'))
    }

    return RDE


def df_summary(dct0, dct100, dct350, dct750):
    #get distance values
    dis1 = dct100.get("Distance(m):", "")
    dis2 = dct350.get("Distance(m):", "")
    dis3 = dct750.get("Distance(m):", "")

    rdh0 = dct0.get("P(eruption in hr)", "")
    rdh1 = dct100.get("Total risk dying in hour:", "")
    rdh2 = dct350.get("Total risk dying in hour:", "")
    rdh3 = dct750.get("Total risk dying in hour:", "")

    tb_final = {'Distance (m)': [0, dis1 , dis2, dis3],
                'Risk dying in hour': [rdh0, rdh1, rdh2, rdh3]}
    df_final = pd.DataFrame(data=tb_final)

    #calculate slope and intercept
    x1 = df_final['Distance (m)']
    y1 = np.log(df_final['Risk dying in hour'])
    m, c = np.polyfit(x1, y1, 1)

    return df_final, round(m, 4), round(c, 4)

def summary_plots(df_s, dct_s, cal):
    inp1 = dct_s.get("Volcano", "")
    inp2 = dct_s.get("Elicitation date", "")
    inp3 = int(dct_s.get("Elicitation (day/s)", ""))

    if inp3 ==0:
        inp3 = int(dct_s.get("duration (week/s)", ""))
        inp3 = str(inp3) + " week/s"
    else:
        inp3 = str(inp3) + " day/s"


    x1 = df_s['Distance (m)']
    y1 = df_s['Risk dying in hour']
    y2 = np.log(df_s['Risk dying in hour'])

    trace1 = go.Scatter(
        x=x1,
        y=y1,
        mode='markers',
        name='Data')

    # linear model
    m, c = np.polyfit(x1, y2, 1)
    #print(m,c)

    # add the linear fit on top
    trace0 = go.Scatter(
        x=x1,
        y=np.exp(m * x1 + c),
        mode="lines",
        marker=go.scatter.Marker(color='rgb(31, 119, 180)'),
        name='Fit'
    )

    data = [trace0, trace1]
    tit = inp1 + " risk (" + cal + " calc): valid " + inp2 + " for " + inp3
    layout = go.Layout(
        title=tit,
        xaxis_title="Distance (m)",
        yaxis_title="Hourly risk of dying from eruption",
        yaxis_type="log",
        yaxis=go.layout.YAxis(
            dtick=1,
            # tick0 = 0.0000001,
            range=[-6, 0],
            autorange=False,
            showexponent='all',
            exponentformat='E'
        )
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    fig.show()
