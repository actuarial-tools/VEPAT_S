from unittest import TestCase
import pandas
import numpy as np
import math
from utils_vepat import cal_vpt, table_vpt, table_stat_vpt
from pandas._testing import assert_frame_equal


class Test(TestCase):
    def test_cal_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, minG, maxG)
        df2 = table_stat_vpt(df1)

        response = cal_vpt(df2=df2,elc=2,du=4)

        self.assertEqual(first=response["P(eruption in period)"], second=0.22799999999999998)
        self.assertEqual(first=response["P(no erupt. in period)"], second=0.772)
        self.assertEqual(first=response["P(no eruption in hr)"], second=0.995)

    def test_table_stat_vpt(self):
        #adding a comment to see what's wrong with git ...
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df2= {'Stat': ['Mean', 'Median', '84th percentile'],
              'Best Guess': [0.188, 0.190, 0.228],
              'Min': [0.074, 0.05, ""],
              'Max': [0.355, 0.4, ""]}
        d_test = pandas.DataFrame(data=df2)

        df1 = table_vpt(pNo, bestG, minG, maxG)

        response = table_stat_vpt(df1)

        assert_frame_equal(response, d_test, check_dtype=False)
