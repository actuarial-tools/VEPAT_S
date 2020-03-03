import pandas as pd
import numpy as np
import math
import pathlib
import os, sys
from copy import deepcopy
import utils_vepat as utiv

class riskcals(object):
    def __init__(self, *fname, **kwargs):
        self.metadata = {}
        self._set_path_metadata(*fname)
        for kw, arg in kwargs.items():
            self.set_metadata(kw, arg)

    def _set_path_metadata(self, *fname):
        for fn in fname:
            fn = pathlib.Path(fn)
            if "path" not in self.metadata or self.metadata["path"] is None:
                self.set_metadata("path", [fn])
            else:
                self.set_metadata("path", [fn])


class risk_cal(riskcals):
    
    def __init__(self, dr):
        self.data = utiv.table_phit()
        self.dr = dr
        #self.phit_cal()
        
    def phit_cal(self):
        self.data['Area'] = self.data['Sqln']**2
        self.data['Phit_abv'] = math.pi * ((self.data['Bdia'] + self.data['Pdia']).div(self.data['Sqln'], axis = 0) **2)
        self.data['Phit_side'] = (self.data['Bdia'] + self.data['Pdia']).div(self.data['Sqln'], axis = 0)
        # self.data['Gmean'] = gmean(self.data.iloc[:, 4:5], axis = 1)
        self.data['Gmean'] = (self.data['Phit_abv'] * self.data['Phit_side']) ** (1/2)
        
        if self.dr == 'above':
                self.data['P_hit'] = self.data['Phit_abv']
        elif self.dr == 'side':
                print("side")
                self.data['P_hit']  = self.data['Phit_side']
        else:
                self.data['P_hit'] = self.data['Gmean']

    @classmethod
    def from_input(cls):
        return cls(
            input("Select missile direction from - above / side / geometric:")
            
        )
