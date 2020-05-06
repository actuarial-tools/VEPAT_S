from unittest import TestCase
import pandas as pd
from pcal_vepat import PcalsVepat
from volcano import volcano
import utils_vepat as utiv
from pandas._testing import assert_frame_equal
from whiteIsland import white_island


class Testrisk_cal(TestCase):

    def setUp(self):
        self.dr = "geometric"
        dfp1 = {'Boulder diameter (m)': [0.2, 0.3, 0.4],
                'Person diameter (m)': [1, 1, 1],
                'Square length (m)': [30, 30, 30],
                'Area (m^2)': [900, 900, 900],
                'P(hit) Above': [0.005026548, 0.005899213, 0.006841691],
                'P(hit) Side': [0.04, 0.043333333, 0.046666667],
                'P(hit) Geometric mean': [0.014179631, 0.015988513, 0.017868377],
                'P(hit)': [0.014179631, 0.015988513, 0.017868377]}
        self.d_test = pd.DataFrame(data=dfp1)

    def test_phit_cal(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        df1 = v.table_phit()
        p_hit = PcalsVepat(self.dr)
        p_hit.load_dfs(df1, df2=None)
        response = p_hit.phit_cal()

        assert_frame_equal(response, self.d_test, check_dtype=False)


    def test_ballis_cal(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        # P of death from one ballistics: tables & calculations
        df1 = v.table_phit()
        p_hit = PcalsVepat(self.dr)
        p_hit.load_dfs(df1, df2=None)
        phit_tbl = p_hit.phit_cal()
        #print(phit_tbl)

        cng = white_island(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                                  eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        # generate ballistics dfs with initial input parameters
        df100, df350, df750 = cng.table_ballis()
        p_hit.load_dfs(phit_tbl, df100)
        response = p_hit.ballis_cal()

        df_balls = {'Eruption size': ["Small", "Moderate", "Large"],
                  'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                  'P(given eruption, exposure to near vent processes)': [0, 0.1, 1],
                  'P(given exposure, death from near vent processes)': [0.9, 0.9, 1],
                  'P(given eruption, death from near vent processes)': [0, 0.09, 1],
                  'P(death from near vent processes in hr)': [0, 0.00000429807, 0.00000530625]}
        ball_test = pandas.DataFrame(data=df_balls)
        assert_frame_equal(response, ball_test, check_dtype=False)


