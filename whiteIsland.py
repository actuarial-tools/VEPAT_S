from volcano import volcano
from pcal_vepat import PcalsVepat
import pandas as pd
import numpy as np
import math



class white_island(volcano):

    def __init__(self, elc, du, eldate, filename, volcano):
        super().__init__(elc, du, volcano, eldate, filename)



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



    def risk_dying_dicts(self):  # here dis = distance = 100, 350, 750m depending on the input dfs/ obps: observation point/calt = calculation type
        rde_100strd = utiv.risk_dying_dicts(self.ball_100m, self.dis1strd, 100, "Overlooking lake", cal_type1, df1=self.near_vent)

        for i in 0, 1, 2:
            if i == 0:
                RDE_sml = self.risk_dying_cal(df2, df3, df1, val=i)
            elif i == 1:
                RDE_med = self.risk_dying_cal(df2, df3, df1, val=i)
            else:
                RDE_lrg = self.risk_dying_cal(df2, df3, df1, val=i)

        TRDE = RDE_sml + RDE_med + RDE_lrg  # total risk of dying in hour

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













    # # ballistic parameters wrt distance
    # # Note that dis1<dis2<dis3
    # def ballistic_area_dis(self):
    #     # Ballistic diameter (m)
    #     ball_dis1 = [0.3, 0.3, 0.3]
    #     ball_dis2 = [0.2, 0.3, 0.3]
    #     ball_dis3 = [0, 0.2, 0.3]
    #
    #     # Given eruption, # ballistics in reference area
    #     ball_area1 = [5, 50, 200]
    #     ball_area2 = [0.1, 10, 100]
    #     ball_area3 = [0, 5, 10]
    #
    #     self.dc3 = {'bdia1': ball_dis1,
    #                 'bdia2': ball_dis2,
    #                 'bdia3': ball_dis3,
    #                 'bn1': ball_area1,
    #                 'bn2': ball_area2,
    #                 'bn3': ball_area3}
    #     return self.dc3
    #
    # def near_vent_p(self):
    #     pex = [0, 0.1, 1]  # P(given eruption, exposure to near vent processes)
    #     ped = [0.9, 0.9, 1]  # P (given exposure, death from near vent processes)
    #
    #     self.dc4 = {'pex': pex,
    #                 'ped': ped}
    #     return self.dc4
    #
    # def surge_paras(self):
    #     # P(given eruption, exposure to surge - esx) at (dis1) 100, (dis2) 350 and (dis3)750m distance for STANDARD CALCULATION (strd),
    #     # ADJUSTED - MAIN CRATER FLOOR / SOUTHERN SECTOR (adjc) and ADJUSTED - HELICOPTER IN SOUTHERN SECTOR (adjh)
    #     # strd
    #     p_esx_dis1str = [0.01, 0.3, 0.4]
    #     p_esx_dis2str = [0, 0.3, 0.4]
    #     p_esx_dis3str = [0, 0.2, 0.4]
    #     # adjc
    #     p_esx_dis1adjc = [1, 1, 1]
    #     p_esx_dis2adjc = [0.5, 1, 1]
    #     p_esx_dis3adjc = [0, 1, 1]
    #     # adjh
    #     p_esx_dis1adjh = [1, 1, 1]
    #     p_esx_dis2adjh = [0, 0.3, 1]
    #     p_esx_dis3adjh = [0, 0.05, 1]
    #
    #     # P(given exposure, death from surge - exd) at 100m, 350m and 750m distances
    #     p_exd_dis1 = [0.95, 1, 1]
    #     p_exd_dis2 = [0.95, 0.95, 1]
    #     p_exd_dis3 = [0.95, 0.95, 0.95]
    #
    #     self.dc5 = {'p_esx_dis1str': p_esx_dis1str,
    #                 'p_esx_dis2str': p_esx_dis2str,
    #                 'p_esx_dis3str': p_esx_dis3str,
    #                 'p_esx_dis1adjc': p_esx_dis1adjc,
    #                 'p_esx_dis2adjc': p_esx_dis2adjc,
    #                 'p_esx_dis3adjc': p_esx_dis3adjc,
    #                 'p_esx_dis1adjh': p_esx_dis1adjh,
    #                 'p_esx_dis2adjh': p_esx_dis2adjh,
    #                 'p_esx_dis3adjh': p_esx_dis3adjh,
    #                 'p_exd_dis1': p_exd_dis1,
    #                 'p_exd_dis2': p_exd_dis2,
    #                 'p_exd_dis3': p_exd_dis3
    #                 }
    #     return self.dc5
