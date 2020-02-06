import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt
import dash

class myTabs(object):

    def __instancecheck__(self, app):
        self.app = app

    def makeTab1(self):
        tab1 = html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            ),
            html.Div(
                [dcc.Input(id='input-box', type='text'),
                 dcc.Input(id='input-box2', type='text'),
                 dcc.DatePickerSingle(
                     id='date-picker-single',
                     date=dt(2000, 5, 10)
                 )]
            )
        ])

        return tab1

    def makeTab2(self):

        tab2 = html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

        return tab2


