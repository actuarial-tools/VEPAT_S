from volcano import volcano
from pcal_vepat import PcalsVepat
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math



class ruapehu(volcano):

    def __init__(self, elc, du, eldate, filename, volcano):
        super().__init__(elc, du, volcano, eldate, filename)
        # self.df1 = None
        self.erp_cls = self.cal_vpt()
        self.table_nvp = self.table_near_vent_proc()

    # def load_table(self, df2):
    #     self.df2 = df2

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
        p_lrgeruphr = 0.1*p_eruphr
        p_mderuphr = 0.4*p_eruphr
        p_smleruphr = 0.5*p_eruphr

        self.erp_cls = {
            "P(eruption in period)": p_erup,
            "P(no erupt. in period)": p_Nerup,
            "P(no eruption in hr)": float(format(p_Neruphr, '.6g')),  # format(val, '.6g') => give 6 significant digits
            "P(eruption in hr)": float(format(p_eruphr, '.6g')),
            "P(size3 eruption in hr)": float(format(p_smleruphr, '.6g')),
            "P(size4 eruption in hr)": float(format(p_mderuphr, '.6g')),
            "P(size5 eruption in hr)": float(format(p_lrgeruphr, '.6g'))
        }

        return self.erp_cls

    # function to extract values from dictionary: erp_cls
    # def get_p_hourly(self):
    #     # getting P(hourly) from erp_cls
    #     p_small = self.erp_cls.get("P(small eruption in hr)", "")
    #     p_mod = self.erp_cls.get("P(moderate eruption in hr)", "")
    #     p_lrg = self.erp_cls.get("P(large eruption in hr)", "")
    #     return p_small, p_mod, p_lrg

    def table_near_vent_proc(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(size3 eruption in hr)", "")
        p_mod = self.erp_cls.get("P(size4 eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(size5 eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]
        p_erp_expo = self.volcanoConfigData['near_vent_inputs'].get(
            "P(given eruption, exposure to near vent processes)", "")
        p_exo_death = self.volcanoConfigData['near_vent_inputs'].get(
            "P (given exposure, death from near vent processes)", "")

        df_nvp = {'Eruption size': erps,
                  'P(hourly)': p_hrly,
                  'P(given eruption, exposure to near vent processes)': p_erp_expo,
                  'P(given exposure, death from near vent processes)': p_exo_death}
        self.table_nvp = pd.DataFrame(data=df_nvp)
        self.table_nvp['P(given eruption, death from near vent processes)'] = self.table_nvp[
                                                                                  'P(given eruption, exposure to near vent processes)'] * \
                                                                              self.table_nvp[
                                                                                  'P(given exposure, death from near vent processes)']
        self.table_nvp['P(death from near vent processes in hr)'] = self.table_nvp['P(hourly)'] * self.table_nvp[
            'P(given eruption, death from near vent processes)']

        return self.table_nvp



    def table_ballis(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(size3 eruption in hr)", "")
        p_mod = self.erp_cls.get("P(size4 eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(size5 eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]
        bpara = self.volcanoConfigData["Ballistics_inputs"]

        # Ballistic diameter (m)
        ball_dia1 = bpara.get("Ballistic diameter 0km", "")
        ball_dia2 = bpara.get("Ballistic diameter 0.5km", "")
        ball_dia3 = bpara.get("Ballistic diameter 1.3km", "")
        ball_dia4 = bpara.get("Ballistic diameter 2km", "")


        # Given eruption, # ballistics in reference area
        ball_no1 = bpara.get("no ballistics in reference area 0km", "")
        ball_no2 = bpara.get("no ballistics in reference area 0.5km", "")
        ball_no3 = bpara.get("no ballistics in reference area 1.3km", "")
        ball_no4 = bpara.get("no ballistics in reference area 2km", "")

        self.df_ballis1 = self.tbl_ballis(erps, p_hrly, ball_dia1, ball_no1)
        self.df_ballis2 = self.tbl_ballis(erps, p_hrly, ball_dia2, ball_no2)
        self.df_ballis3 = self.tbl_ballis(erps, p_hrly, ball_dia3, ball_no3)
        self.df_ballis4 = self.tbl_ballis(erps, p_hrly, ball_dia4, ball_no4)

        return self.df_ballis1, self.df_ballis2, self.df_ballis3,\
               self.df_ballis4

    # SURGE: 0km/350m/1.3km/ for standard, adjusted crater floor and helicopter in southern sector

    def table_surge(self):
        # getting P(hourly) from erp_cls
        p_small = self.erp_cls.get("P(size3 eruption in hr)", "")
        p_mod = self.erp_cls.get("P(size4 eruption in hr)", "")
        p_lrg = self.erp_cls.get("P(size5 eruption in hr)", "")

        erps = self.volcanoConfigData['near_vent_inputs'].get("Eruption size", "")
        p_hrly = [p_small, p_mod, p_lrg]

        srg_para = self.volcanoConfigData["Surge_inputs"]

        # P(given eruption, exposure to surge) at 100, 350 and 1.3km distance for STANDARD CALCULATION (strd),
        # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR (adjc) and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR (adjh)
        # standard
        p_esx_dis1str = srg_para.get("P(given eruption, exposure to surge)_standard_0km", "")
        p_esx_dis2str = srg_para.get("P(given eruption, exposure to surge)_standard_0.5km", "")
        p_esx_dis3str = srg_para.get("P(given eruption, exposure to surge)_standard_1.3km", "")
        p_esx_dis4str = srg_para.get("P(given eruption, exposure to surge)_standard_2km", "")


        # P(given exposure, death from surge) at 0km, 0.5km and 1.3km distances
        p_exd_dis1 = srg_para.get("P(given exposure, death from surge)_0km", "")
        p_exd_dis2 = srg_para.get("P(given exposure, death from surge)_0.5km", "")
        p_exd_dis3 = srg_para.get("P(given exposure, death from surge)_1.3km", "")
        p_exd_dis4 = srg_para.get("P(given exposure, death from surge)_2km", "")

        # generate all 9 tables:
        self.dis1strd = self.tbl_surge(erps, p_hrly, p_esx_dis1str, p_exd_dis1)
        self.dis2strd = self.tbl_surge(erps, p_hrly, p_esx_dis2str, p_exd_dis2)
        self.dis3strd = self.tbl_surge(erps, p_hrly, p_esx_dis3str, p_exd_dis3)
        self.dis4strd = self.tbl_surge(erps, p_hrly, p_esx_dis4str, p_exd_dis4)

        return self.dis1strd, self.dis2strd, self.dis3strd, self.dis4strd

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
            "Distance(km):": dis,
            "Site description:": obsp,
            "Total risk dying in hour:": float(format(TRDE, '.10g')),
            "Risk dying from size3 eruption in hour:": float(format(RDE_sml, '.5g')),
            "Risk dying from size4 eruption in hour:": float(format(RDE_med, '.5g')),
            "Risk dying from size5 eruption in hour:": float(format(RDE_lrg, '.5g'))
        }

        return self.RDE

    def df_summary(self, dctDis1, dctDis2, dctDis3, dctDis4, cal):
        # get distance values
        dis1 = dctDis1.get("Distance(km):", "")
        dis2 = dctDis2.get("Distance(km):", "")
        dis3 = dctDis3.get("Distance(km):", "")
        dis4 = dctDis4.get("Distance(km):", "")

        #rdh0 = dctDis0.get("P(eruption in hr)", "")
        rdh1 = dctDis1.get("Total risk dying in hour:", "")
        rdh2 = dctDis2.get("Total risk dying in hour:", "")
        rdh3 = dctDis3.get("Total risk dying in hour:", "")
        rdh4 = dctDis4.get("Total risk dying in hour:", "")

        tb_final = {'Distance (km)': [dis1, dis2, dis3, dis4],
                    'Risk dying in hour': [rdh1, rdh2, rdh3,rdh4]}
        self.df_final = pd.DataFrame(data=tb_final)

        # calculate slope and intercept
        x1 = self.df_final['Distance (km)']
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

        x1 = df_s['Distance (km)']
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
            col1 = row['cal type'] + ' (km)'
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





