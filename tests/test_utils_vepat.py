from unittest import TestCase
import pandas
import numpy as np
import math
from utils_vepat import cal_vpt, table_vpt, table_stat_vpt
from pandas._testing import assert_frame_equal



class Test(TestCase): #run this test for elecitation = 1 and duration = 4
    def test_cal_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, Best_guessR, minG, maxG)
        df2 = table_stat_vpt(df1)

        response = cal_vpt(df1,df2=df2,elc=1,du=0)

        self.assertEqual(first=response["P(eruption in period)"], second=0.300),
        self.assertEqual(first=response["P(no erupt. in period)"], second=0.700),
        self.assertEqual(first=response["P(no eruption in hr)"], second=0.985),
        self.assertEqual(first=response["P(eruption in hr)"], second=0.0148),
        self.assertEqual(first=response["P(small eruption in hr)"],second=0.0133),
        self.assertEqual(first=response["P(moderate eruption in hr)"],second=0.00133),
        self.assertEqual(first=response["P(large eruption in hr)"],second=0.000148)



    def test_table_stat_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df2 = {'Stat': ['Mean', 'Median', '84th percentile'],
               'Best Guess': [0.188, 0.190, 0.300],
               'Min': [0.074, 0.05, ""],
               'Max': [0.355, 0.4, ""]}
        d_test = pandas.DataFrame(data=df2)

        df1 = table_vpt(pNo, bestG,Best_guessR, minG, maxG)
        response = table_stat_vpt(df1)

        assert_frame_equal(response, d_test, check_dtype=False)
