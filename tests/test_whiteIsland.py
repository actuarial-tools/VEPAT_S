from unittest import TestCase


class Testwhite_island(TestCase):
    def test_table_ballis(self):
        v = volcano(elc=0, du=4, volcano='WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')

        response = v.table_stat_vpt()
