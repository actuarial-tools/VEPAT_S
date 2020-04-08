from unittest import TestCase
import pandas as pd
import numpy as np
import math
from utils_vepat import table_phit
from pcal_vepat import risk_cal
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
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        dff1 = utiv.table_vpt(pNo, bestG, Best_guessR, minG, maxG)
        dff2 = utiv.table_stat_vpt(dff1)


        df1 = utiv.table_phit()
        p_test = risk_cal(self.dr)
        p_test.load_dfs(df1, df2=None)
        phit_tbl = p_test.phit_cal()

        #print(p_test.data)
        #p_test.data.to_csv('p_test.csv')

        #assert_frame_equal(p_test.data, self.d_test, check_exact=False, check_less_precise=True, check_dtype=False)
        assert_frame_equal(phit_tbl, self.d_test, check_dtype=False)





