from volcano import volcano
from pcal_vepat import PcalsVepat
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math



class white_island(volcano):

    def __init__(self, elc, du, eldate, filename, volcano):
        super().__init__(elc, du, volcano, eldate, filename)
        #self.df1 = None
        self.erp_cls = self.cal_vpt()
        self.table_nvp = self.table_near_vent_proc()

    def doCalculationsPlots(self, pcals, get_inps, base_para, distance1, distance2, distance3,
                            site1, site2, site3, cal_type1, cal_type2, cal_type3 ):
        # calculations for plotting and other, calculations from this function saved as a dictionary
        erp_cals = self.cal_vpt()

        # Table: Near Vent Processes
        near_vent = self.table_near_vent_proc()

        # P of death from one ballistics: tables & calculations
        phit = pcals.PcalsVepat.from_input()
        df1 = get_inps.table_phit()
        phit.load_dfs(df1, df2=None)

        # Tables of Death from one ballistic: 0.2 m/0.3/0.4
        phit_tbl = phit.phit_cal()

        # elecitation statistics plot
        get_inps.elici_plot()
        get_inps.elici_plot_last()

        # generate ballistics dfs with initial input parameters
        df_dis1, df_dis2, df_dis3 = self.table_ballis()

        # ballistics 100m table for statnadrd, adjusted
        phit.load_dfs(df1, df_dis1)
        ball_dis1 = phit.ballis_cal(phit_tbl)

        # ballistics 350m table for statnadrd, adjusted
        phit.load_dfs(df1, df_dis2)
        ball_dis2 = phit.ballis_cal(phit_tbl)

        # ballistics 750m table for statnadrd, adjusted
        phit.load_dfs(df1, df_dis3)
        ball_dis3 = phit.ballis_cal(phit_tbl)

        # generate all the surge tables (9 tables)
        df_srgDis1strd, df_srgDis2strd, df_srgDis3strd, df_srgDis1adjc, df_srgDis2adjc, \
        df_srgDis3adjc, df_srgDis1adjh, df_srgDis2adjh, df_srgDis3adjh = self.table_surge()

        ##risk of dying in an eruption (rde) calculations:
        # inpput parameters: dis = distance (=100, 350, 750m depending on the input dfs)/ obps: observation point/calt = calculation type
        # cal_type1 calculation
        rde_Dis1strd = self.risk_dying_dicts(ball_dis1, df_srgDis1strd, distance1, site1, cal_type1, df1=near_vent)
        rde_Dis2strd = self.risk_dying_dicts(ball_dis2, df_srgDis2strd, distance2, site2, cal_type1, df1=None)
        rde_Dis3strd = self.risk_dying_dicts(ball_dis3, df_srgDis3strd, distance3, site3, cal_type1, df1=None)

        # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR
        rde_Dis1adjc = self.risk_dying_dicts(ball_dis1, df_srgDis1adjc, distance1, site1, cal_type2, df1=near_vent)
        rde_Dis2adjc = self.risk_dying_dicts(ball_dis2, df_srgDis2adjc, distance2, site2, cal_type2, df1=None)
        rde_Dis3adjc = self.risk_dying_dicts(ball_dis3, df_srgDis3adjc, distance3, site3, cal_type2, df1=None)

        # ADJUSTED - HELICOPTER IN SOUTHERN SECTOR
        rde_Dis1adjh = self.risk_dying_dicts(ball_dis1, df_srgDis1adjh, distance1, site1, cal_type3, df1=near_vent)
        rde_Dis2adjh = self.risk_dying_dicts(ball_dis2, df_srgDis2adjh, distance2, site2, cal_type3, df1=None)
        rde_Dis3adjh = self.risk_dying_dicts(ball_dis3, df_srgDis3adjh, distance3, site3, cal_type3, df1=None)

        # generate summary tables and calculations
        pd.options.display.float_format = '{:.3g}'.format
        summary_strd, slope_strd, yincp_strd, cal_strd = self.df_summary(erp_cals, rde_Dis1strd, rde_Dis2strd,
                                                                        rde_Dis3strd, cal_type1)
        summary_adjc, slope_adjc, yincp_adjc, cal_adjc = self.df_summary(erp_cals, rde_Dis1adjc, rde_Dis2adjc,
                                                                        rde_Dis3adjc, cal_type2)
        summary_adjh, slope_adjh, yincp_adjh, cal_adjh = self.df_summary(erp_cals, rde_Dis1adjh, rde_Dis2adjh,
                                                                        rde_Dis3adjh, cal_type3)

        # generate volcano specific plots
        # risk summary plots
        self.summary_plots(summary_strd, cal_type1)
        self.summary_plots(summary_adjc, cal_type2)
        self.summary_plots(summary_adjh, cal_type3)

        # Generate summary table with slopes, intercepts and calculation type

        tb_smry = {'cal type': [cal_type1, cal_type2, cal_type3],
                   'slope': [slope_strd, slope_adjc, slope_adjh],
                   'yinc': [yincp_strd, yincp_adjc, yincp_adjh]}
        df_smry = pd.DataFrame(data=tb_smry)

        # Generate final risk zone table
        riskzn = self.riskzn(df_smry)







    def cal_vpt(self):
        p_erup = self.df2.iloc[2]['Best Guess']  # P(eruption in period):
        p_Nerup = 1 - p_erup  # P(no erupt. in period):

        if self.elc > 0:
            B6 = self.elc
        else:
            if self.du > 0:
                B6 = self.du * 7
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

        self.erp_cls = {
            "P(eruption in period)": p_erup,
            "P(no erupt. in period)": p_Nerup,
            "P(no eruption in hr)": float(format(p_Neruphr, '.6g')),  # format(val, '.6g') => give 6 significant digits
            "P(eruption in hr)": float(format(p_eruphr, '.6g')),
            "P(small eruption in hr)": float(format(p_smleruphr, '.6g')),
            "P(moderate eruption in hr)": float(format(p_mderuphr, '.6g')),
            "P(large eruption in hr)": float(format(p_lrgeruphr, '.6g'))
        }

        return self.erp_cls



    def table_near_vent_proc(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(small eruption in hr)", "")
        p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(large eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]
        p_erp_expo = self.volcanoConfigData['near_vent_inputs'].get("P(given eruption, exposure to near vent processes)", "")
        p_exo_death = self.volcanoConfigData['near_vent_inputs'].get("P (given exposure, death from near vent processes)", "")

        df_nvp = {'Eruption size': erps,
                  'P(hourly)': p_hrly,
                  'P(given eruption, exposure to near vent processes)': p_erp_expo,
                  'P(given exposure, death from near vent processes)': p_exo_death}
        self.table_nvp = pd.DataFrame(data=df_nvp)
        self.table_nvp['P(given eruption, death from near vent processes)'] = self.table_nvp['P(given eruption, exposure to near vent processes)'] * \
                                                                            self.table_nvp['P(given exposure, death from near vent processes)']
        self.table_nvp['P(death from near vent processes in hr)'] = self.table_nvp['P(hourly)'] * self.table_nvp['P(given eruption, death from near vent processes)']

        return self.table_nvp

    def table_ballis(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(small eruption in hr)", "")
        p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(large eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]
        bpara = self.volcanoConfigData["Ballistics_inputs"]

        # Ballistic diameter (m)
        ball_dia1 = bpara.get("Ballistic diameter 100m", "")
        ball_dia2 = bpara.get("Ballistic diameter 350m", "")
        ball_dia3 = bpara.get("Ballistic diameter 750m", "")

        # Given eruption, # ballistics in reference area
        ball_no1 = bpara.get("no ballistics in reference area 100m", "")
        ball_no2 = bpara.get("no ballistics in reference area 350m", "")
        ball_no3 = bpara.get("no ballistics in reference area 750m", "")

        self.df_ballis1 = self.tbl_ballis(erps, p_hrly, ball_dia1, ball_no1)
        self.df_ballis2 = self.tbl_ballis(erps, p_hrly, ball_dia2, ball_no2)
        self.df_ballis3 = self.tbl_ballis(erps, p_hrly, ball_dia3, ball_no3)

        return self.df_ballis1, self.df_ballis2, self.df_ballis3

    # SURGE: 100m/350m/750m/ for standard, adjusted crater floor and helicopter in southern sector

    def table_surge(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(small eruption in hr)", "")
        p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(large eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]

        srg_para = self.volcanoConfigData["Surge_inputs"]

        # P(given eruption, exposure to surge) at 100, 350 and 750m distance for STANDARD CALCULATION (strd),
        # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR (adjc) and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR (adjh)
        # standard
        p_esx_dis1str = srg_para.get("P(given eruption, exposure to surge)_standard_100m", "")
        p_esx_dis2str = srg_para.get("P(given eruption, exposure to surge)_standard_350m", "")
        p_esx_dis3str = srg_para.get("P(given eruption, exposure to surge)_standard_750m", "")

        # adjusted crater
        p_esx_dis1adjc = srg_para.get("P(given eruption, exposure to surge)_adjustedCrater_100m", "")
        p_esx_dis2adjc = srg_para.get("P(given eruption, exposure to surge)_adjustedCrater_350m", "")
        p_esx_dis3adjc = srg_para.get("P(given eruption, exposure to surge)_adjustedCrater_750m", "")
        #
        # adjusted helicopter
        p_esx_dis1adjh = srg_para.get("P(given eruption, exposure to surge)_adjustedHelicopter_100m", "")
        p_esx_dis2adjh = srg_para.get("P(given eruption, exposure to surge)_adjustedHelicopter_350m", "")
        p_esx_dis3adjh = srg_para.get("P(given eruption, exposure to surge)_adjustedHelicopter_750m", "")

        # P(given exposure, death from surge) at 100m, 350m and 750m distances
        p_exd_dis1 = srg_para.get("P(given exposure, death from surge)_100m", "")
        p_exd_dis2 = srg_para.get("P(given exposure, death from surge)_350m", "")
        p_exd_dis3 = srg_para.get("P(given exposure, death from surge)_750m", "")

        # generate all 9 tables:
        self.dis1strd = self.tbl_surge(erps, p_hrly, p_esx_dis1str, p_exd_dis1)
        self.dis2strd = self.tbl_surge(erps, p_hrly, p_esx_dis2str, p_exd_dis2)
        self.dis3strd = self.tbl_surge(erps, p_hrly, p_esx_dis3str, p_exd_dis3)

        self.dis1adjc = self.tbl_surge(erps, p_hrly, p_esx_dis1adjc, p_exd_dis1)
        self.dis2adjc = self.tbl_surge(erps, p_hrly, p_esx_dis2adjc, p_exd_dis2)
        self.dis3adjc = self.tbl_surge(erps, p_hrly, p_esx_dis3adjc, p_exd_dis3)

        self.dis1adjh = self.tbl_surge(erps, p_hrly, p_esx_dis1adjh, p_exd_dis1)
        self.dis2adjh = self.tbl_surge(erps, p_hrly, p_esx_dis2adjh, p_exd_dis2)
        self.dis3adjh = self.tbl_surge(erps, p_hrly, p_esx_dis3adjh, p_exd_dis3)

        return self.dis1strd, self.dis2strd, self.dis3strd, self.dis1adjc, self.dis2adjc, self.dis3adjc, self.dis1adjh, self.dis2adjh, self.dis3adjh

    def risk_dying_dicts(self, df2, df3, dis, obsp, calt, df1):  # here dis = distance = 100, 350, 750m depending on the input dfs/ obps: observation point/calt = calculation type\
        for i in 0, 1, 2:
            if i == 0:
                RDE_sml = self.risk_dying_cal(df2, df3, df1, val=i)
            elif i == 1:
                RDE_med = self.risk_dying_cal(df2, df3, df1, val=i)
            else:
                RDE_lrg = self.risk_dying_cal(df2, df3, df1, val=i)

        TRDE = RDE_sml + RDE_med + RDE_lrg  # total risk of dying in hour

        self.RDE = {
            "Calculation:": calt,
            "Distance(m):": dis,
            "Site description:": obsp,
            "Total risk dying in hour:": float(format(TRDE, '.10g')),
            "Risk dying from small eruption in hour:": float(format(RDE_sml, '.5g')),
            "Risk dying from moderate eruption in hour:": float(format(RDE_med, '.5g')),
            "Risk dying from large eruption in hour:": float(format(RDE_lrg, '.5g'))
        }

        return self.RDE

    def df_summary(self, dct0, dct100, dct350, dct750, cal):
        # get distance values
        dis1 = dct100.get("Distance(m):", "")
        dis2 = dct350.get("Distance(m):", "")
        dis3 = dct750.get("Distance(m):", "")

        rdh0 = dct0.get("P(eruption in hr)", "")
        rdh1 = dct100.get("Total risk dying in hour:", "")
        rdh2 = dct350.get("Total risk dying in hour:", "")
        rdh3 = dct750.get("Total risk dying in hour:", "")

        tb_final = {'Distance (m)': [0, dis1, dis2, dis3],
                    'Risk dying in hour': [rdh0, rdh1, rdh2, rdh3]}
        self.df_final = pd.DataFrame(data=tb_final)

        # calculate slope and intercept
        x1 = self.df_final['Distance (m)']
        y1 = np.log(self.df_final['Risk dying in hour'])
        self.m, self.c = np.polyfit(x1, y1, 1)

        return self.df_final, round(self.m, 6), round(self.c, 6), cal

    def summary_plots(self, df_s, cal):
        inp1 = self.volcano
        inp2 = self.eldate
        inp3 = int(self.elc)

        if inp3 == 0:
            inp3 = int(self.du)
            inp3 = str(inp3) + " week/s"
        else:
            inp3 = str(inp3) + " day/s"

        x1 = df_s['Distance (m)']
        x1max = df_s['Distance (m)'].max()
        y1 = df_s['Risk dying in hour']
        y2 = np.log(df_s['Risk dying in hour'])

        trace1 = go.Scatter(
            x=x1,
            y=y1,
            mode='markers',
            marker_symbol='diamond',
            marker_color="rgba(0,0,0,0.5)",
            name='Data')

        # linear model
        m, c = np.polyfit(x1, y2, 1)
        # print(m,c)

        # add the linear fit on top
        trace0 = go.Scatter(
            x=x1,
            y=np.exp(m * x1 + c),
            mode="lines",
            line=dict(width=2, dash='dot', color="rgba(0,0,0,0.8)"),
            name='Fit'
        )

        data = [trace0, trace1]
        tit = inp1 + " risk (" + cal + " calc): valid " + inp2 + " for " + inp3
        layout = go.Layout(
            title=tit,
            xaxis_title="Distance (m)",
            yaxis_title="Hourly risk of dying from eruption",
            yaxis_type="log",
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=go.layout.YAxis(
                dtick=1,
                # tick0 = 0.0000001,
                range=[-6, 0],
                autorange=False,
                showexponent='all',
                exponentformat='E'
            ),
            xaxis = go.layout.XAxis(
                dtick=100,
                range=[0, x1max + 100],
                autorange=False
            )
        )

        self.fig = go.Figure(
            data=data,
            layout=layout
        )

        self.fig.update_xaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                         tickcolor='black', ticklen=4, mirror=True)
        self.fig.update_yaxes(showline=True, linewidth=0.8, linecolor='black', ticks="outside", tickwidth=0.8,
                         tickcolor='black', ticklen=4, mirror=True)
        self.fig.update_layout(
            shapes=[
                # 1st highlight during Feb 4 - Feb 6
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    y0=0.000001,
                    x0=0,
                    y1=0.00001,
                    x1=1,
                    fillcolor="Lightgreen",
                    name='< 10-5 (just field intention form): > 520 m',
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ),
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    y0=0.00001,
                    x0=0,
                    y1=0.0001,
                    x1=1,
                    fillcolor="Lightyellow",
                    name='10-4 - 10-5 (VSA approval): < 520 m',
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ),
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    y0=0.0001,
                    x0=0,
                    y1=0.001,
                    x1=1,
                    fillcolor="lightpink",
                    name='10-3 - 10-4 (GMS & VSA approval): N/A',
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ),

                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    y0=0.001,
                    x0=0,
                    y1=1,
                    x1=1,
                    fillcolor="lightblue",
                    name='> 10-3 (exclusion zone): N/A',
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                )

            ]
        )

        self.fig.show()

    # final risk zone table
    def riskzn(self, df2):
        HRF = self.volcanoConfigData["final_zone_estimate"]["Hourly risk of fatality"]
        # hrf1 = HRF[0]
        # hrf2 = HRF[1]
        # hrf3 = HRF[2]
        GNSstff = self.volcanoConfigData["final_zone_estimate"]["GNS Staff access sign-off"]
        tb_riskzone = {'Hourly risk of fatality': ['{0:1.1E}'.format(HRF[0], 'E'), '{0:1.1E}'.format(HRF[1], 'E'), '{0:1.1E}'.format(HRF[2], 'E')],
                       'GNS Staff access sign-off': GNSstff}

        df1 = pd.DataFrame(data=tb_riskzone)

        for index, row in df2.iterrows():
            col1 = row['cal type'] + ' (m)'
            val2 = float(row['yinc'])
            val3 = float(row['slope'])

            dfh = pd.DataFrame([])
            list1 = []
            for hrf in df1['Hourly risk of fatality']:
                # print(hrf)
                val1 = 10 * round(((np.log(float(hrf)) - val2) / val3) / 10, 0)
                dfh = dfh.append(pd.DataFrame({col1: val1}, index=[0]), ignore_index=True)
                list1 = dfh[col1].tolist()
            df1[col1] = list1

        return df1











