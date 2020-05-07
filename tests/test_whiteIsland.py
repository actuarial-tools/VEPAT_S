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




# no need to test table_ballis as ballis_hit is already tested
# def test_table_ballis(self):
#     v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
#                 eldate='21 January 2020', filename='../config_whiteIsland.JSON')
#
#     response = v.table_stat_vpt()