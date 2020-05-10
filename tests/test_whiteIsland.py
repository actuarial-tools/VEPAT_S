from unittest import TestCase
import pandas as pd
from pcal_vepat import PcalsVepat
from volcano import volcano
import utils_vepat as utiv
from pandas._testing import assert_frame_equal
from whiteIsland import white_island

class Testwhite_island(TestCase):

    def test_table_surge(self):
        cng = white_island(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                           eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        df_srg100strd, df_srg350strd, df_srg750strd, df_srg100adjc, df_srg350adjc, \
        df_srg750adjc, df_srg100adjh, df_srg350adjh, df_srg750adjh = cng.table_surge()

        response = df_srg100strd

        df_surge = {'Eruption size': ["Small", "Moderate", "Large"],
                    'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                    'P(given eruption, exposure to surge)': [0.01, 0.3, 0.4],
                    'P(given exposure, death from surge)': [0.95, 1, 1],
                    'P(given eruption, death from surge)': [0.0095, 0.3, 0.4],
                    'P(death from surge in hr)': [0.00000453685, 0.0000143269,0.0000021225]}
        surge_test = pd.DataFrame(data=df_surge)
        assert_frame_equal(response, surge_test, check_dtype=False)

    def test_cal_vpt(self):
        v = white_island(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
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
        v = white_island(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                         eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        ball_dia = [0.2, 0.3, 0.4]
        person_dia = [1, 1, 1]
        sq_lng = [30, 30, 30]

        d1 = {'boulder diameter': ball_dia,
              'person diameter': person_dia,
              'square length': sq_lng}
        d_test = pd.DataFrame(data=d1)
        response = v.table_phit()
        assert_frame_equal(response, d_test, check_dtype=False)

    def test_table_near_vent_proc(self):
        v = white_island(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                         eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        response = v.table_near_vent_proc()

        df_nvp = {'Eruption size': ["Small", "Moderate", "Large"],
                  'P(hourly)': [0.000477563, 0.0000477563, 0.00000530625],
                  'P(given eruption, exposure to near vent processes)': [0, 0.1, 1],
                  'P(given exposure, death from near vent processes)': [0.9, 0.9, 1],
                  'P(given eruption, death from near vent processes)': [0, 0.09, 1],
                  'P(death from near vent processes in hr)': [0, 0.00000429807, 0.00000530625]}
        nvp_test = pd.DataFrame(data=df_nvp)
        assert_frame_equal(response, nvp_test, check_dtype=False)






# no need to test table_ballis as ballis_hit is already tested
# def test_table_ballis(self):
#     v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
#                 eldate='21 January 2020', filename='../config_whiteIsland.JSON')
#
#     response = v.table_stat_vpt()