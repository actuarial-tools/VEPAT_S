from unittest import TestCase

from volcano import volcano


class Testvolcano(TestCase):
    def test_read_config(self):
        v = volcano(elc = 0, du = 4, volcano = 'WHAKAARI / WHITE ISLAND',
                    eldate='21 January 2020', filename='../config_whiteIsland.JSON')
        wsdata = v.read_config(filename='../config_whiteIsland.JSON')
        self.assertSequenceEqual(wsdata["elicitation_inputs"]['Person'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertSequenceEqual(wsdata["elicitation_inputs"]['Best guess'], [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3])


    def test_inp_para(self):
        self.fail()

    def test_table_vpt(self):
        self.fail()
