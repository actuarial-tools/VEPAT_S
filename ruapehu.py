from volcano import volcano
from pcal_vepat import PcalsVepat
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math



class ruapehu(volcano):

    def __init__(self, elc, du, eldate, filename, volcano):
        super().__init__(elc, du, volcano, eldate, filename)
        self.df1 = None


    def load_table(self, df2):
        self.df2 = df2




    def table_ballis(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(small eruption in hr)", "")
        p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(large eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]
        bpara = self.volcanoConfigData["Ballistics_inputs"]

        # Ballistic diameter (m)
        ball_dia1 = bpara.get("Ballistic diameter 0km", "")
        ball_dia2 = bpara.get("Ballistic diameter 350m", "")
        ball_dia3 = bpara.get("Ballistic diameter 1.3km", "")

        # Given eruption, # ballistics in reference area
        ball_no1 = bpara.get("no ballistics in reference area 0km", "")
        ball_no2 = bpara.get("no ballistics in reference area 350m", "")
        ball_no3 = bpara.get("no ballistics in reference area 1.3km", "")

        self.df_ballis1 = self.tbl_ballis(erps, p_hrly, ball_dia1, ball_no1)
        self.df_ballis2 = self.tbl_ballis(erps, p_hrly, ball_dia2, ball_no2)
        self.df_ballis3 = self.tbl_ballis(erps, p_hrly, ball_dia3, ball_no3)

        return self.df_ballis1, self.df_ballis2, self.df_ballis3

    # SURGE: 0km/350m/1.3km/ for standard, adjusted crater floor and helicopter in southern sector

    def table_surge(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(small eruption in hr)", "")
        p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(large eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]

        srg_para = self.volcanoConfigData["Surge_inputs"]

        # P(given eruption, exposure to surge) at 100, 350 and 1.3km distance for STANDARD CALCULATION (strd),
        # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR (adjc) and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR (adjh)
        # standard
        p_esx_dis1str = srg_para.get("P(given eruption, exposure to surge)_standard_0km", "")
        p_esx_dis2str = srg_para.get("P(given eruption, exposure to surge)_standard_0.5km", "")
        p_esx_dis3str = srg_para.get("P(given eruption, exposure to surge)_standard_1.3km", "")


        # P(given exposure, death from surge) at 0km, 0.5km and 1.3km distances
        p_exd_dis1 = srg_para.get("P(given exposure, death from surge)_0km", "")
        p_exd_dis2 = srg_para.get("P(given exposure, death from surge)_0.5km", "")
        p_exd_dis3 = srg_para.get("P(given exposure, death from surge)_1.3km", "")

        # generate all 9 tables:
        self.dis1strd = self.tbl_surge(erps, p_hrly, p_esx_dis1str, p_exd_dis1)
        self.dis2strd = self.tbl_surge(erps, p_hrly, p_esx_dis2str, p_exd_dis2)
        self.dis3strd = self.tbl_surge(erps, p_hrly, p_esx_dis3str, p_exd_dis3)

        return self.dis1strd, self.dis2strd, self.dis3strd

    def risk_dying_dicts(self, df2, df3, dis, obsp, calt, df1):  # here dis = distance = 0, 0.5, 1.3km depending on the input dfs/ obps: observation point/calt = calculation type\
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
            "Total risk dying in hour:": float(format(TRDE, '.3g')),
            "Risk dying from small eruption in hour:": float(format(RDE_sml, '.3g')),
            "Risk dying from moderate eruption in hour:": float(format(RDE_med, '.3g')),
            "Risk dying from large eruption in hour:": float(format(RDE_lrg, '.3g'))
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
        y1 = df_s['Risk dying in hour']
        y2 = np.log(df_s['Risk dying in hour'])

        trace1 = go.Scatter(
            x=x1,
            y=y1,
            mode='markers',
            name='Data')

        # linear model
        m, c = np.polyfit(x1, y2, 1)
        # print(m,c)

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

        self.fig = go.Figure(
            data=data,
            layout=layout
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





