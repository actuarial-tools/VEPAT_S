import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from myGuiElements import myDropDown, myContainer, myButton


class reportTab(object):
    def __init__(self, id):
        self.id = id
        self.element = dcc.Tab(label='Report',
                               children=[], id=id)