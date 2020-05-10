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





