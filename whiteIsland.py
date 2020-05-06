from volcano import volcano
import pandas as pd



class white_island(volcano):

    def __init__(self, elc, du, eldate, filename, volcano):
        super().__init__(elc, du, volcano, eldate, filename)



    def tbl_ballis(self, dct1, lst1, lst2, lst3):
        df_ballp = {'Eruption size': dct1,
                    'P(hourly)': lst1,
                    'Ballistic diameter (m)': lst2,
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': lst3}
        # 'P(given eruption, death from ballistics)': p_erp_death_ball}
        df_bp = pd.DataFrame(data=df_ballp)
        return df_bp

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
        #return erps, bpara, p_hrly










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
