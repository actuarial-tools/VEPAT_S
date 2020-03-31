from unittest import TestCase
import pandas as pd
import numpy as np
import math
from utils_vepat import table_phit
from pcal_vepat import risk_cal
from pandas._testing import assert_frame_equal


class Testrisk_cal(TestCase):

    def setUp(self):
        self.dr = "geometric"
        dfp1 = {'Bdia': [0.2, 0.3, 0.4],
                'Pdia': [1, 1, 1],
                'Sqln': [30, 30, 30],
                'Area': [900, 900, 900],
                'Phit_abv': [0.005026548, 0.005899213, 0.006841691],
                'Phit_side': [0.04, 0.043333333, 0.046666667],
                'Gmean': [0.014179631, 0.015988513, 0.017868377],
                'P_hit': [0.014179631, 0.015988513, 0.017868377]}
        self.d_test = pd.DataFrame(data=dfp1)



    def test_phit_cal(self):

        print(self.d_test)
        self.d_test.to_csv('ddtest.csv')
        p_test = risk_cal(self.dr)
        p_test.phit_cal()

        print(p_test.data)
        #p_test.data.to_csv('p_test.csv')

        #assert_frame_equal(p_test.data, self.d_test, check_exact=False, check_less_precise=True, check_dtype=False)
        assert_frame_equal(p_test.data, self.d_test, check_dtype=False)





