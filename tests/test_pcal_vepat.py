from unittest import TestCase
import pandas as pd
from pcal_vepat import PcalsVepat
from volcano import volcano
import utils_vepat as utiv
from pandas._testing import assert_frame_equal


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





