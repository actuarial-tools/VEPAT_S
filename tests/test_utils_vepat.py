from unittest import TestCase

from utils_vepat import cal_vpt, table_vpt, table_stat_vpt


class Test(TestCase):
    def test_cal_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, minG, maxG)
        df2 = table_stat_vpt(df1)

        response = cal_vpt(df2=df2,elc=1 ,du=4)

        self.assertEqual(first=response["P(eruption in period)"], second=0.3)
        self.assertEqual(first=response["P(no erupt. in period)"], second=0.7)
        self.assertEqual(first=response["P(no eruption in hr)"], second=0.993)




class Test(TestCase):
    def test_table_stat_vpt(self):
        pNo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bestG = [0.1, 0.15, 0.15, 0.15, 0.18, 0.2, 0.2, 0.2, 0.25, 0.3]
        minG = [0.05, 0.05, 0.05, 0.05, 0.11, 0.05, 0.1, 0.13, 0.1, 0.05]
        maxG = [0.2, 0.25, 0.25, 0.4, 0.25, 0.4, 0.4, 0.4, 0.4, 0.6]

        df1 = table_vpt(pNo, bestG, minG, maxG)
        df2 = table_stat_vpt(df1)

        # self.assertEqual()
