import pandas as pd
import numpy as np
import math



class PcalsVepat(object):
    
    def __init__(self, dr):
        #self.data = utiv.table_phit()
        self.df1 = None
        self.dr = dr
        self.df2 = None
        self.df3 = None
        self.dfb1 = None


    def load_dfs(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def phit_cal(self):
        self.df1['Area'] = self.df1['square length']**2
        self.df1['Phit_abv'] = math.pi * ((self.df1['boulder diameter'] + self.df1['person diameter']).div(self.df1['square length'], axis = 0) **2)
        self.df1['Phit_side'] = (self.df1['boulder diameter'] + self.df1['person diameter']).div(self.df1['square length'], axis = 0)
        # self.df1['Gmean'] = gmean(self.df1.iloc[:, 4:5], axis = 1)
        self.df1['Gmean'] = (self.df1['Phit_abv'] * self.df1['Phit_side']) ** (1/2)

        
        if self.dr == 'above':
                self.df1['P_hit'] = self.df1['Phit_abv']
        elif self.dr == 'side':
                print("side")
                self.df1['P_hit']  = self.df1['Phit_side']
        else:
                self.df1['P_hit'] = self.df1['Gmean']

        self.df1.columns = ['Boulder diameter (m)', 'Person diameter (m)', 'Square length (m)', 'Area (m^2)', 'P(hit) Above',\
                     'P(hit) Side', 'P(hit) Geometric mean', 'P(hit)']
        return self.df1

    @classmethod
    def from_input(cls):
        return cls(
            input("Select missile direction from - above / side / geometric:")
            
        )


    def ballis_cal(self):
        self.df3 = self.df1[['Boulder diameter (m)', 'P(hit)']]
        self.df3.set_index('Boulder diameter (m)', inplace=True)
        self.dfb1= self.df2.merge(
                     self.df3,
                     left_on='Ballistic diameter (m)',
                     right_index=True,
                     how='left',
                     sort=False
        )
        #BRA:Given eruption, # ballistics in reference area
        self.bpr = self.dfb1['Given eruption, # ballistics in reference area']
       # self.dfb1['P(given eruption, death from ballistics)'] = (1 - self.dfb1['P_hit'])
        self.dfb1['P(given eruption, death from ballistics)'] = (1 - self.dfb1['P(hit)']).pow(self.bpr, axis=0)
        self.dfb1['P(given eruption, death from ballistics)'] = 1 - self.dfb1['P(given eruption, death from ballistics)']
        self.dfb1['P(death from ballistics in hr)'] = self.dfb1['P(hourly)'] * self.dfb1['P(given eruption, death from ballistics)']
        self.dfb1 = self.dfb1.drop(['P(hit)'], axis=1)
        return self.dfb1



