import pandas as pd
import numpy as np
import math
import pathlib
import os, sys
from copy import deepcopy
import utils_vepat as utiv

# class riskcals(object):
#     def __init__(self, *fname, **kwargs):
#         self.metadata = {}
#         self._set_path_metadata(*fname)
#         for kw, arg in kwargs.items():
#             self.set_metadata(kw, arg)
#
#     def _set_path_metadata(self, *fname):
#         for fn in fname:
#             fn = pathlib.Path(fn)
#             if "path" not in self.metadata or self.metadata["path"] is None:
#                 self.set_metadata("path", [fn])
#             else:
#                 self.set_metadata("path", [fn])


class risk_cal(object):
    
    def __init__(self, dr):
        #self.data = utiv.table_phit()
        self.df1 = None
        self.dr = dr
        self.df2 = None


    def load_dfs(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def phit_cal(self):
        self.df1['Area'] = self.df1['Sqln']**2
        self.df1['Phit_abv'] = math.pi * ((self.df1['Bdia'] + self.df1['Pdia']).div(self.df1['Sqln'], axis = 0) **2)
        self.df1['Phit_side'] = (self.df1['Bdia'] + self.df1['Pdia']).div(self.df1['Sqln'], axis = 0)
        # self.df1['Gmean'] = gmean(self.df1.iloc[:, 4:5], axis = 1)
        self.df1['Gmean'] = (self.df1['Phit_abv'] * self.df1['Phit_side']) ** (1/2)
        
        if self.dr == 'above':
                self.df1['P_hit'] = self.df1['Phit_abv']
        elif self.dr == 'side':
                print("side")
                self.df1['P_hit']  = self.df1['Phit_side']
        else:
                self.df1['P_hit'] = self.df1['Gmean']

        return self.df1

    @classmethod
    def from_input(cls):
        return cls(
            input("Select missile direction from - above / side / geometric:")
            
        )


    def ball100cal(self):
        self.df3 = self.df1[['Bdia', 'P_hit']]
        self.df3.set_index('Bdia', inplace=True)
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
        self.dfb1['P(given eruption, death from ballistics)'] = (1 - self.dfb1['P_hit']).pow(self.bpr, axis=0)
        self.dfb1['P(given eruption, death from ballistics)'] = 1 - self.dfb1['P(given eruption, death from ballistics)']
        self.dfb1['P(death from ballistics in hr)'] = self.dfb1['P(hourly)'] * self.dfb1['P(given eruption, death from ballistics)']
        self.dfb1 = self.dfb1.drop(['P_hit'], axis=1)


