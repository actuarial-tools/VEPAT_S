from unittest import TestCase
import pandas
from pandas._testing import assert_frame_equal
from pandas._testing import assert_series_equal

from volcano import volcano


class Testvolcano(TestCase):
    def test_read_config(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        wsdata = v.read_config(filename='../config_whiteIsland.JSON')
        self.assertSequenceEqual(wsdata["elicitation_inputs"]['Person'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertSequenceEqual(wsdata["elicitation_inputs"]['Best guess'],
                                 [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3])

    def test_inp_para(self):
        vol = input('Volcano:')
        confg = input('Configuration file (JSON):')  # config_whiteIsland.JSON
        eldate = input('Elicitation date:')
        print("Only enter one of Elicitation (days/s) or Duration (week/s), if non enter 0")

        elc = int(input('Elicitation (day/s):'))
        if elc > 0:
            du = 0
        else:
            du = int(input('Duration (week/s):'))

        v = volcano(elc, du, vol, eldate, confg)
        response = v.inp_para()
        self.assertEqual(first=response["Elicitation (day/s)"], second=0),

    def test_table_vpt(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        response = v.table_vpt()

        df1 = {"Person": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
               "Best guess": [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3],
               "Best guess repeat": [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3],
               "Min": [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05],
               "Max": [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6],
               "Error low": [0.05, 0.1, 0.1, 0.1, 0.07, 0.15, 0.1, 0.07, 0.15, 0.25],
               "Error high": [0.1, 0.1, 0.1, 0.25, 0.07, 0.2, 0.2, 0.2, 0.15, 0.3]}
        df_test = pandas.DataFrame(data=df1)
        assert_frame_equal(response, df_test, check_dtype=False)

    def test_table_stat_vpt(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        response = v.table_stat_vpt()

        df2 = {'Stat': ['Mean', 'Median', '84th percentile'],
               'Best Guess': [0.188, 0.190, 0.300],
               'Min': [0.074, 0.05, ""],
               'Max': [0.355, 0.4, ""]}
        df2_test = pandas.DataFrame(data=df2)
        assert_frame_equal(response, df2_test, check_dtype=False)

    def test_cal_vpt(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        response = v.cal_vpt()

        self.assertEqual(first=response["P(eruption in period)"], second=0.300),
        self.assertEqual(first=response["P(no erupt. in period)"], second=0.700),
        self.assertEqual(first=response["P(no eruption in hr)"], second=0.999469),
        self.assertEqual(first=response["P(eruption in hr)"], second=0.000530625),
        self.assertEqual(first=response["P(small eruption in hr)"], second=0.000477563),
        self.assertEqual(first=response["P(moderate eruption in hr)"], second=0.0000477563),
        self.assertEqual(first=response["P(large eruption in hr)"], second=0.00000530625)

    def test_table_phit(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        ball_dia = [0.2, 0.3, 0.4]
        person_dia = [1, 1, 1]
        sq_lng = [30, 30, 30]

        d1 = {'boulder diameter': ball_dia,
              'person diameter': person_dia,
              'square length': sq_lng}
        d_test = pandas.DataFrame(data=d1)
        response = v.table_phit()
        assert_frame_equal(response, d_test, check_dtype=False)

    def test_table_near_vent_proc(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        response = v.table_near_vent_proc()

        df_nvp = {'Eruption size': ["Small", "Moderate", "Large"],
                  'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                  'P(given eruption, exposure to near vent processes)': [0, 0.1, 1],
                  'P(given exposure, death from near vent processes)': [0.9, 0.9, 1],
                  'P(given eruption, death from near vent processes)': [0, 0.09, 1],
                  'P(death from near vent processes in hr)': [0, 0.00000429807, 0.00000530625]}
        nvp_test = pandas.DataFrame(data=df_nvp)
        assert_frame_equal(response, nvp_test, check_dtype=False)



