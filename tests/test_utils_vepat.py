from unittest import TestCase
import pandas
import numpy as np
import math
from utils_vepat import cal_vpt, table_vpt, table_stat_vpt, table_phit, get_p_hourly, tbl_ballis
from pandas._testing import assert_frame_equal


class Test(TestCase):  # run this test for elecitation = 1 and duration = 4
    def test_cal_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, Best_guessR, minG, maxG)
        df2 = table_stat_vpt(df1)

        response = cal_vpt(df2=df2, elc=0, du=4)

        self.assertEqual(first=response["P(eruption in period)"], second=0.300),
        self.assertEqual(first=response["P(no erupt. in period)"], second=0.700),
        self.assertEqual(first=response["P(no eruption in hr)"], second=0.999469),
        self.assertEqual(first=response["P(eruption in hr)"], second=0.000530625),
        self.assertEqual(first=response["P(small eruption in hr)"], second=0.000477563),
        self.assertEqual(first=response["P(moderate eruption in hr)"], second=0.0000477563),
        self.assertEqual(first=response["P(large eruption in hr)"], second=0.00000530625)

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

        df1 = table_vpt(pNo, bestG, Best_guessR, minG, maxG)
        response = table_stat_vpt(df1)

        assert_frame_equal(response, d_test, check_dtype=False)

    def test_table_phit(self):
        ball_dia = [0.2, 0.3, 0.4]
        person_dia = [1, 1, 1]
        sq_lng = [30, 30, 30]

        d1 = {'Bdia': ball_dia,
              'Pdia': person_dia,
              'Sqln': sq_lng}
        d_test = pandas.DataFrame(data=d1)
        response = table_phit()
        assert_frame_equal(response, d_test, check_dtype=False)


    def test_table_ballis(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        Best_guessR = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, Best_guessR, minG, maxG)
        df2 = table_stat_vpt(df1)

        erp_cals = cal_vpt(df2=df2, elc=0, du=4)

        p_small = get_p_hourly(erp_cals)[0]
        p_mod = get_p_hourly(erp_cals)[1]
        p_lrg = get_p_hourly(erp_cals)[2]

        erps = ["Small", "Moderate", "Large"]
        p_hrly = [p_small, p_mod, p_lrg]

        # Ballistic diameter (m)
        ball_dia100 = [0.3, 0.3, 0.3]
        ball_dia350 = [0.2, 0.3, 0.3]
        ball_dia750 = [0, 0.2, 0.3]

        # Given eruption, # ballistics in reference area
        ball_area100 = [5, 50, 200]
        ball_area350 = [0.1, 10, 100]
        ball_area750 = [0, 5, 10]

        response1 = tbl_ballis(erps, p_hrly, ball_dia100, ball_area100)
        response2 = tbl_ballis(erps, p_hrly, ball_dia350, ball_area350)
        response3 = tbl_ballis(erps, p_hrly, ball_dia750, ball_area750)

        dfb1 = {'Eruption size': ["Small", "Moderate", "Large"],
                    'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                    'Ballistic diameter (m)': [0.3, 0.3, 0.3],
                    # BRA:Given eruption, # ballistics in reference area
                    'Given eruption, # ballistics in reference area': [5, 50, 200]}
        # 'P(given eruption, death from ballistics)': p_erp_death_ball}
        df_test1 = pandas.DataFrame(data=dfb1)

        dfb2 = {'Eruption size': ["Small", "Moderate", "Large"],
                'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                'Ballistic diameter (m)': [0.2, 0.3, 0.3],
                # BRA:Given eruption, # ballistics in reference area
                'Given eruption, # ballistics in reference area': [0.1, 10, 100]}
        # 'P(given eruption, death from ballistics)': p_erp_death_ball}
        df_test2 = pandas.DataFrame(data=dfb2)

        dfb3 = {'Eruption size': ["Small", "Moderate", "Large"],
                'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                'Ballistic diameter (m)': [0, 0.2, 0.3],
                # BRA:Given eruption, # ballistics in reference area
                'Given eruption, # ballistics in reference area': [0, 5, 10]}
        # 'P(given eruption, death from ballistics)': p_erp_death_ball}
        df_test3 = pandas.DataFrame(data=dfb3)

        assert_frame_equal(response1, df_test1, check_dtype=False)
        assert_frame_equal(response2, df_test2, check_dtype=False)
        assert_frame_equal(response3, df_test3, check_dtype=False)



